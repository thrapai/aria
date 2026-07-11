import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

from aria.core.context import ARIAContext
from aria.core.errors import ExtensionExecutionError, InputResolutionError
from aria.core.logger import write_json
from aria.core.templates import render_value
from aria.extensions.registry import default_registry
from aria.types.workflow import InputSpec, Step, Workflow


def run_workflow(workflow: Workflow, workflow_path: Path, cli_inputs: dict[str, Any]) -> dict[str, Any]:
    started_at = _now()
    run_dir = Path(".aria") / "runs" / started_at
    steps_dir = run_dir / "steps"
    steps_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(workflow_path, run_dir / "workflow.yml")

    context = ARIAContext(
        inputs=_resolve_inputs(workflow.inputs, cli_inputs), providers=workflow.providers, run_dir=run_dir
    )
    write_json(run_dir / "inputs.json", context.inputs)
    registry = default_registry()
    metadata = {"workflow_name": workflow.name, "started_at": started_at, "status": "running", "steps": []}

    try:
        for step in workflow.steps:
            step_meta = {"id": step.id, "uses": step.uses, "status": "running", "started_at": _now()}
            metadata["steps"].append(step_meta)
            if step.for_each is None:
                output = _run_step(step, context, registry, steps_dir, step.id)
            else:
                items = render_value(step.for_each, context, native=True)
                if not isinstance(items, list):
                    raise ExtensionExecutionError(f"Step '{step.id}' for_each must render to a list")
                output = []
                previous_item = context.item
                try:
                    for index, item in enumerate(items):
                        context.item = item
                        output.append(_run_step(step, context, registry, steps_dir, f"{step.id}.{index}"))
                finally:
                    context.item = previous_item
            context.steps[step.id] = {"output": output}
            write_json(steps_dir / f"{step.id}.output.json", output)
            step_meta.update({"status": "success", "finished_at": _now()})

        outputs = render_value(workflow.outputs, context, native=True)
        write_json(run_dir / "outputs.json", outputs)
        metadata.update({"status": "success", "finished_at": _now()})
        write_json(run_dir / "metadata.json", metadata)
        return outputs
    except Exception as exc:
        if metadata["steps"]:
            metadata["steps"][-1].update({"status": "failed", "finished_at": _now()})
            metadata["failed_step"] = metadata["steps"][-1]["id"]
        metadata.update({"status": "failed", "finished_at": _now(), "error": str(exc)})
        write_json(run_dir / "metadata.json", metadata)
        if isinstance(exc, (ExtensionExecutionError, InputResolutionError)):
            raise
        raise ExtensionExecutionError(str(exc)) from exc


def _resolve_inputs(specs: dict[str, InputSpec], cli_inputs: dict[str, Any]) -> dict[str, Any]:
    values = {}
    for key, spec in specs.items():
        if key in cli_inputs:
            values[key] = _coerce(cli_inputs[key], spec.type)
        elif spec.default is not None:
            values[key] = spec.default
        elif spec.required:
            raise InputResolutionError(f"Missing required input: {key}")
    return values


def _run_step(step: Step, context: ARIAContext, registry: Any, steps_dir: Path, artifact_id: str) -> dict[str, Any]:
    step_input = render_value(step.with_, context)
    write_json(steps_dir / f"{artifact_id}.input.json", step_input)
    if step.uses == "ai.generate" and "prompt" in step_input:
        (steps_dir / f"{artifact_id}.prompt.txt").write_text(step_input["prompt"], encoding="utf-8")
    output = registry.get(step.uses).run(step_input, context)
    write_json(steps_dir / f"{artifact_id}.output.json", output)
    return output


def _coerce(value: Any, type_: str) -> Any:
    if type_ == "number":
        return float(value) if "." in str(value) else int(value)
    if type_ == "boolean":
        if str(value).lower() in {"true", "1", "yes"}:
            return True
        if str(value).lower() in {"false", "0", "no"}:
            return False
        raise InputResolutionError(f"Invalid boolean input: {value}")
    return value


def _now() -> str:
    return datetime.now().replace(microsecond=0).isoformat().replace(":", "-")
