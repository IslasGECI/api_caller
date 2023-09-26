from api_caller import cli

import requests_mock
from typer.testing import CliRunner

runner = CliRunner()


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "write-probability-progress-figure " in result.stdout

    result = runner.invoke(cli, ["write-csv-probability", "--help"])
    assert result.exit_code == 0
    assert "--input-path " in result.stdout
    assert " Path of input data " in result.stdout
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstrap by window " in result.stdout
    assert "--output-path " in result.stdout
    assert " Path of csv file to write " in result.stdout
    assert "--window-length " in result.stdout
    assert " Number of months by window " in result.stdout

    result = runner.invoke(cli, ["write-probability-progress-figure", "--help"])
    assert result.exit_code == 0
    assert "--input-path " in result.stdout
    assert " Path of input data " in result.stdout
    assert "--output-path " in result.stdout
    assert " Path of figure to write " in result.stdout


def tests_writ_csv_probability_entrypoint():
    with requests_mock.Mocker() as m:
        m.get("http://eradication_progress:10000/write_probability_figure", text="Response 200")

        runner.invoke(
            cli,
            [
                "write-probability-progress-figure",
                "--input-path",
                "probabilities.csv",
                "--output-path",
                "figure.png",
            ],
        )
        assert m.call_count == 1
