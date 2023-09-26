from api_caller import cli

from typer.testing import CliRunner

runner = CliRunner()


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "write-probability-progress-figure " in result.stdout

    result = runner.invoke(cli, ["write-csv-probability", "--help"])
    assert result.exit_code == 0
    assert "--input-path " in result.stdout
    assert "--bootstrapping-number " in result.stdout
    assert "--output-path " in result.stdout
    assert "--window-length " in result.stdout

    result = runner.invoke(cli, ["write-probability-progress-figure", "--help"])
    assert result.exit_code == 0
    assert "--input-path " in result.stdout
    assert "--output-path " in result.stdout
