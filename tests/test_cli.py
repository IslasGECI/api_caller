from geci_caller import (
    cli,
    plot_cpue_vs_cum_captures,
    plot_custom_cpue_vs_cum_captures,
    write_probability_progress_figure,
)
import geci_test_tools as gtt
from typer.testing import CliRunner
import json
import os
import requests_mock
from PIL import Image

runner = CliRunner()


def tests_write_population_status_from_mixed_methods():
    command = "write-population-status-from-mixed-methods"
    result = get_command_help(command)
    assert result.exit_code == 0

    output_path = "population_status_mixed_methods.json"
    result = runner.invoke(
        cli,
        [
            command,
            "--first-method-status",
            "tests/data/population_status_terrestrial_hunting.json",
            "--second-method-status",
            "tests/data/population_status_aerial_hunting.json",
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout


def tests_write_bootstrap_progress_intervals_json():
    command = "write-bootstrap-progress-intervals"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstraps " in result.stdout
    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            "tests/data/feral_goat_capture_effort.csv",
            "--bootstrapping-number",
            10,
            "--output-path",
            "progress_intervals.json",
        ],
    )
    assert "200" in result.stdout


def get_command_help(command: str):
    return runner.invoke(cli, [command, "--help"])


def tests_write_aerial_monitoring():
    command = "write-aerial-monitoring"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstraps " in result.stdout
    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            "effort_captures.csv",
            "--bootstrapping-number",
            10,
            "--output-path",
            "filtered_data.json",
        ],
    )
    assert "500" in result.stdout


def tests_filter_by_method():
    command = "filter-by-method"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)
    assert " Extraction method " in result.stdout

    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            "effort_captures.csv",
            "--method",
            "aerea",
            "--output-path",
            "filtered_data.csv",
        ],
    )
    assert "500" in result.stdout


def tests_write_population_status():
    command = "write-population-status"
    input_path = "tests/data/feral_goat_capture_effort.csv"
    output_path = "population_status.json"

    if os.path.exists(output_path):
        os.remove(output_path)

    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)
    assert " Number of bootstraps " in result.stdout

    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            input_path,
            "--bootstrapping-number",
            10,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    with open(output_path) as f:
        data = json.load(f)
    assert data["capturas"] == 11
    assert data["progress_probability"] == 1.0


def test_call_entrypoint():
    command = "write-csv-probability"
    result = get_command_help(command)
    assert_successful_command(result)
    assert_input_path_argument(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstrap by window " in result.stdout
    assert "--output-path " in result.stdout
    assert " Path of csv file to write " in result.stdout
    assert "--window-length " in result.stdout
    assert " Number of months by window " in result.stdout


def tests_write_probability_progress_figure():
    command = "write-probability-progress-figure"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)


def tests_plot_cpue_vs_cum_captures():
    command = "plot-cpue-vs-cum-captures"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)


def tests_plot_comparative_catch_curves():
    command = "plot-comparative-catch-curves"
    result = get_command_help(command)
    assert "--socorro-path " in result.stdout
    assert " Path of Socorro data " in result.stdout
    assert "--guadalupe-path " in result.stdout
    assert " Path of Guadalupe data " in result.stdout
    assert_successful_command(result)
    assert_output_path_argument(result)

    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/plot_comparative_catch_curves"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "plot-comparative-catch-curves",
                "--socorro-path",
                "cumulatives_socorro.csv",
                "--guadalupe-path",
                "cumulatives_guadalupe.csv",
                "--output-path",
                "figure.png",
            ],
        )
        assert m.call_count == 1
        assert "200" in result.stdout


def tests_write_csv_probability_entrypoint():
    input_path = "tests/data/feral_goat_capture_effort.csv"
    output_path = "probabilities.csv"

    if os.path.exists(output_path):
        os.remove(output_path)

    with requests_mock.Mocker() as m:
        entrypoint = "http://islasgeci.org:100/write_effort_and_captures_with_probability"
        mock_response = [
            {"Esfuerzo": 10, "Capturas": 5, "Fecha": "2023-12-01", "prob": 0.75},
            {"Esfuerzo": 12, "Capturas": 3, "Fecha": "2024-12-01", "prob": 0.65},
        ]
        m.post(entrypoint, json=mock_response)

        runner.invoke(
            cli,
            [
                "write-csv-probability",
                "--input-path",
                input_path,
                "--bootstrapping-number",
                2,
                "--window-length",
                6,
                "--output-path",
                output_path,
            ],
        )
        assert m.call_count == 1

        assert os.path.exists(output_path)
        import pandas as pd

        df = pd.read_csv(output_path)
        assert len(df) == 2
        assert "Esfuerzo" in df.columns
        assert "Capturas" in df.columns
        assert "Fecha" in df.columns
        assert "prob" in df.columns


def tests_write_probability_figure_entrypoint():
    input_path = "tests/data/progress_probability_tests.csv"
    format = "png"
    output_path = f"probability_progress_figure.{format}"
    gtt.if_exist_remove(output_path)
    result = runner.invoke(
        cli,
        [
            "write-probability-progress-figure",
            "--input-path",
            input_path,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    assert "200" in result.stdout

    response = write_probability_progress_figure(input_path, output_path)
    assert "http://islasgeci.org:100/write_probability_figure" in response.url
    gtt.assert_exist(output_path)

    assert_figure_format(format, output_path)


def tests_plot_cumulative_series_cpue_by_flight_entrypoint():
    result = runner.invoke(cli, ["plot-cumulative-series-cpue-by-flight", "--help"])
    assert_command_with_input_and_output_paths(result)

    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/plot_cumulative_series_cpue_by_flight"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "plot-cumulative-series-cpue-by-flight",
                "--input-path",
                "probabilities.csv",
                "--output-path",
                "figure.png",
            ],
        )
        assert m.call_count == 1
        assert "200" in result.stdout


def tests_plot_cpue_vs_cum_captures_entrypoint():
    format = "eps"
    output_path = f"figure_cpue_vs_cum.{format}"
    input_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    gtt.if_exist_remove(output_path)
    result = runner.invoke(
        cli,
        [
            "plot-cpue-vs-cum-captures",
            "--input-path",
            input_path,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    assert "200" in result.stdout

    response = plot_cpue_vs_cum_captures(input_path, output_path)
    assert "http://islasgeci.org:100/plot_cpue_vs_cum_captures" in response.url
    gtt.assert_exist(output_path)

    assert_figure_format(format, output_path)


def assert_figure_format(format, output_path):
    with Image.open(output_path) as img:
        assert img.format == format.upper()


def tests_plot_custom_cpue_vs_cum_captures_entrypoint():
    result = runner.invoke(cli, ["plot-custom-cpue-vs-cum-captures", "--help"])
    assert_command_with_input_and_output_paths(result)
    assert " Path of config file " in result.stdout

    input_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    config_path = "tests/data/hunt_config.json"
    format = "eps"
    output_path = f"figure.{format}"
    result = runner.invoke(
        cli,
        [
            "plot-custom-cpue-vs-cum-captures",
            "--input-path",
            input_path,
            "--config-path",
            config_path,
            "--output-path",
            output_path,
        ],
    )
    response = plot_custom_cpue_vs_cum_captures(input_path, config_path, output_path)
    assert result.exit_code == 0
    assert "200" in result.stdout
    assert "http://islasgeci.org:100/plot_custom_cpue_vs_cum_captures" in response.url

    assert_figure_format(format, output_path)


def tests_version():
    obtained_result = get_command_help("version")
    assert_successful_command(obtained_result)
    obtained_result = runner.invoke(cli, ["version"])
    assert "0.16.0" in obtained_result.stdout


def assert_command_with_input_and_output_paths(result):
    assert_successful_command(result)
    assert_input_path_argument(result)
    assert_output_path_argument(result)


def assert_successful_command(result):
    assert result.exit_code == 0


def assert_input_path_argument(results):
    assert "--input-path " in results.stdout
    assert " Path of input data " in results.stdout


def assert_output_path_argument(result):
    assert "--output-path " in result.stdout
    assert " Path of figure to write " in result.stdout
