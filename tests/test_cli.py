from api_caller import cli

from typer.testing import CliRunner

runner = CliRunner()


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")

    assert result.exit_code == 0
    assert "service-name" in result.stdout
