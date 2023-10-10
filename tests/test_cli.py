from geci_caller import cli

import requests_mock
from typer.testing import CliRunner

runner = CliRunner()


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")
    assert result.exit_code == 0
    assert "write-probability-progress-figure " in result.stdout

    result = runner.invoke(cli, ["write-csv-probability", "--help"])
    assert result.exit_code == 0
    assert_input_path_argument(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstrap by window " in result.stdout
    assert "--output-path " in result.stdout
    assert " Path of csv file to write " in result.stdout
    assert "--window-length " in result.stdout
    assert " Number of months by window " in result.stdout

    result = runner.invoke(cli, ["write-probability-progress-figure", "--help"])
    assert result.exit_code == 0
    assert_input_path_argument(result)
    assert_output_path_argument(result)

    result = runner.invoke(cli, ["plot-cpue-vs-cum-captures", "--help"])
    assert result.exit_code == 0
    assert_input_path_argument(result)
    assert_output_path_argument(result)


def assert_input_path_argument(results):
    assert "--input-path " in results.stdout
    assert " Path of input data " in results.stdout


def assert_output_path_argument(result):
    assert "--output-path " in result.stdout
    assert " Path of figure to write " in result.stdout


def tests_write_csv_probability_entrypoint():
    with requests_mock.Mocker() as m:
        m.get(
            "http://eradication_progress:10000/write_effort_and_captures_with_probability",
            text="Response 200",
        )

        runner.invoke(
            cli,
            [
                "write-csv-probability",
                "--input-path",
                "effort_captures.csv",
                "--bootstrapping-number",
                2,
                "--window-length",
                6,
                "--output-path",
                "probabilities.csv",
            ],
        )
        assert m.call_count == 1
        expected_url = "http://eradication_progress:10000/write_effort_and_captures_with_probability?input_path=effort_captures.csv&bootstrapping_number=2&output_path=probabilities.csv&window_length=6"
        print(m.request_history[0].url)
        assert m.request_history[0].url == expected_url


def tests_write_probability_figure_entrypoint():
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
        expected_url = "http://eradication_progress:10000/write_probability_figure?input_path=probabilities.csv&output_path=figure.png"
        assert m.request_history[0].url == expected_url
