from typer.testing import CliRunner

from aria import __version__
from aria.cli import app

runner = CliRunner()


def test_version_command_shows_version():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert f"thrapai-aria {__version__}" in result.stdout


def test_update_command_shows_all_methods_when_unspecified():
    result = runner.invoke(app, ["update"])
    assert result.exit_code == 0
    assert "pipx: pipx upgrade thrapai-aria" in result.stdout
    assert "pip: python -m pip install -U thrapai-aria" in result.stdout
    assert "uv: uv tool upgrade thrapai-aria" in result.stdout


def test_update_command_shows_selected_method():
    result = runner.invoke(app, ["update", "--method", "pipx"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "pipx upgrade thrapai-aria"
