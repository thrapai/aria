from pathlib import Path

from aic.core.runner import run_workflow
from aic.extensions.builtins.utils import JsonParse, TextChunk
from aic.types.workflow import Workflow


def test_file_write_workflow_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow_path = Path("workflow.yml")
    workflow_path.write_text(
        """
version: "0.1"
name: hello
inputs:
  name:
    type: string
    required: true
steps:
  - id: write
    uses: file.write
    with:
      path: hello.txt
      content: "Hello {{ inputs.name }}"
outputs:
  file: "{{ steps.write.output.path }}"
""",
        encoding="utf-8",
    )
    workflow = Workflow.model_validate(
        {
            "version": "0.1",
            "name": "hello",
            "inputs": {"name": {"type": "string", "required": True}},
            "steps": [
                {
                    "id": "write",
                    "uses": "file.write",
                    "with": {"path": "hello.txt", "content": "Hello {{ inputs.name }}"},
                }
            ],
            "outputs": {"file": "{{ steps.write.output.path }}"},
        }
    )

    assert run_workflow(workflow, workflow_path, {"name": "Thomas"}) == {"file": "hello.txt"}
    assert Path("hello.txt").read_text(encoding="utf-8") == "Hello Thomas"
    assert list(Path(".aic/runs").glob("*/metadata.json"))


def test_for_each_runs_step_for_each_item(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    workflow_path = Path("workflow.yml")
    workflow_path.write_text(
        """
version: "0.1"
name: loop
inputs:
  names:
    default:
      - one
      - two
steps:
  - id: write
    uses: file.write
    for_each: "{{ inputs.names }}"
    with:
      path: "{{ item }}.txt"
      content: "Hello {{ item }}"
outputs:
  files: "{{ steps.write.output }}"
""",
        encoding="utf-8",
    )
    workflow = Workflow.model_validate(
        {
            "version": "0.1",
            "name": "loop",
            "inputs": {"names": {"default": ["one", "two"]}},
            "steps": [
                {
                    "id": "write",
                    "uses": "file.write",
                    "for_each": "{{ inputs.names }}",
                    "with": {"path": "{{ item }}.txt", "content": "Hello {{ item }}"},
                }
            ],
            "outputs": {"files": "{{ steps.write.output }}"},
        }
    )

    assert run_workflow(workflow, workflow_path, {}) == {
        "files": [{"path": "one.txt", "bytes": 9}, {"path": "two.txt", "bytes": 9}]
    }
    assert Path("one.txt").read_text(encoding="utf-8") == "Hello one"
    assert Path("two.txt").read_text(encoding="utf-8") == "Hello two"


def test_json_parse_parses_valid_json(tmp_path):
    assert JsonParse().run({"text": '{"name":"Thomas"}'}, None)["value"] == {"name": "Thomas"}


def test_text_chunk_chunks_text(tmp_path):
    assert TextChunk().run({"text": "abcdef", "size": 3, "overlap": 1}, None)["chunks"] == ["abc", "cde", "ef"]


def test_text_chunk_splits_on_delimiter(tmp_path):
    assert TextChunk().run({"text": "# A\ntext\n# B\ntext", "delimiter": "\n# "}, None)["chunks"] == [
        "# A\ntext",
        "\n# B\ntext",
    ]


def test_text_chunk_packs_delimiter_chunks_to_size(tmp_path):
    assert TextChunk().run({"text": "aa\nbb\ncc", "delimiter": "\n", "size": 5}, None)["chunks"] == [
        "aa\nbb",
        "\ncc",
    ]
