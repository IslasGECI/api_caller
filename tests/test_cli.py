from api_caller import cli

from typer.testing import CliRunner

runner = CliRunner()


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0

    result = runner.invoke(cli, ["write-csv-probability", "--help"])
    assert result.exit_code == 0
    assert "--input-path " in result.stdout
    assert "--bootstrapping-number " in result.stdout
    assert "--output-path " in result.stdout
    assert "--window-length " in result.stdout
