from geci_caller import (
    cli,
    plot_comparative_catch_curves,
    plot_comparative_yearly_cpue,
    plot_cpue_vs_cum_captures,
    plot_cumulative_cpue_series_by_season,
    plot_cumulative_series_cpue_by_flight,
    plot_custom_cpue_vs_cum_captures,
    write_csv_probability,
    write_probability_progress_figure,
)
import geci_test_tools as gtt
from typer.testing import CliRunner
import json
import os
from PIL import Image
import pytest
from requests import HTTPError

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
    input_path = "tests/data/monitoreo_cabras_magdalena.csv"
    output_path = "aerial_monitoring.json"
    gtt.if_exist_remove(output_path)
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
    assert "200" in result.stdout
    gtt.assert_exist(output_path)


def tests_filter_by_method():
    command = "filter-by-method"
    result = get_command_help(command)
    assert_command_with_input_and_output_paths(result)
    assert " Extraction method " in result.stdout

    input_path = "tests/data/terrestrial_hunting.csv"
    output_path = "filtered_data.csv"
    gtt.if_exist_remove(output_path)
    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            input_path,
            "--method",
            "Cacería terrestre",
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout
    gtt.assert_exist(output_path)


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

    socorro_path = "tests/data/cumulative_effort_and_captures_for_year.csv"
    guadalupe_path = "tests/data/cumulative_effort_and_captures_for_year_guadalupe.csv"
    output_path = "figure.png"
    result = runner.invoke(
        cli,
        [
            "plot-comparative-catch-curves",
            "--socorro-path",
            socorro_path,
            "--guadalupe-path",
            guadalupe_path,
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout
    response = plot_comparative_catch_curves(socorro_path, guadalupe_path, output_path)
    assert "http://islasgeci.org:100/plot_comparative_catch_curves" in response.url
    gtt.assert_exist(output_path)


def tests_plot_comparative_yearly_cpue():
    command = "plot-comparative-yearly-cpue"
    result = get_command_help(command)
    assert "--socorro-path " in result.stdout
    assert " Path of Socorro data " in result.stdout
    assert "--guadalupe-path " in result.stdout
    assert " Path of Guadalupe data " in result.stdout
    assert_successful_command(result)
    assert_output_path_argument(result)

    socorro_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    guadalupe_path = "tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv"
    output_path = "comparative_cpue.png"
    result = runner.invoke(
        cli,
        [
            "plot-comparative-yearly-cpue",
            "--socorro-path",
            socorro_path,
            "--guadalupe-path",
            guadalupe_path,
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout
    response = plot_comparative_yearly_cpue(socorro_path, guadalupe_path, output_path)
    assert "http://islasgeci.org:100/plot_comparative_yearly_cpue" in response.url
    gtt.assert_exist(output_path)


def tests_write_instantaneous_and_cumulative_cpue():
    command = "write-instantaneous-and-cumulative-cpue"
    result = get_command_help(command)
    assert_successful_command(result)
    assert_input_path_argument(result)
    assert_output_path_argument(result, message="Path to write")
    assert_argument(
        result, option_name="resolution", message="Temporal resolution: monthly, season"
    )
    input_path = "tests/data/esfuerzo_capturas_gatos_guadalupe_ISO_for_tests.csv"
    output_path = "cpue_and_cumulative_cpue.csv"

    gtt.if_exist_remove(output_path)

    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            input_path,
            "--output-path",
            output_path,
            "--resolution",
            "monthly",
        ],
    )
    assert result.exit_code == 0
    assert os.path.exists(output_path)


def tests_write_csv_probability_entrypoint():
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
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    output_path = "probabilities.csv"

    gtt.if_exist_remove(output_path)

    bootstrapping_number = 2
    window_length = 6
    result = runner.invoke(
        cli,
        [
            "write-csv-probability",
            "--input-path",
            input_path,
            "--bootstrapping-number",
            bootstrapping_number,
            "--window-length",
            window_length,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    assert os.path.exists(output_path)

    response = write_csv_probability(
        input_path, bootstrapping_number, output_path, window_length, None
    )
    assert "http://islasgeci.org:100/write_effort_and_captures_with_probability" in response.url

    resolution = 4
    response = write_csv_probability(
        input_path, bootstrapping_number, output_path, window_length, resolution
    )
    assert "http://islasgeci.org:100/write_effort_and_captures_with_probability" in response.url


def tests_write_posterior_results():
    input_path = "tests/data/data_effort_captures_for_model.json"
    parameters_path = "tests/data/init_captures_effort_model.json"
    output_path = "posteriors.csv"

    gtt.if_exist_remove(output_path)

    result = runner.invoke(
        cli,
        [
            "write-posterior-results",
            "--input-path",
            input_path,
            "--initial-parameters-path",
            parameters_path,
            "--output-path",
            output_path,
        ],
    )
    assert result.exit_code == 0
    assert os.path.exists(output_path)


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


def tests_write_instantaneous_and_cumulative_cpue_time_series_plot():
    command = "write-instantaneous-and-cumulative-cpue-time-series-plot"
    result = runner.invoke(cli, [command, "--help"])
    assert_command_with_input_and_output_paths(result)
    output_path = "cumulative_by_season.png"
    input_path = "tests/data/cpue_and_cumulative_cpue.csv"
    result = runner.invoke(
        cli,
        [
            command,
            "--input-path",
            input_path,
            "--output-path",
            output_path,
        ],
    )
    assert_succesfull_command(result)
    gtt.assert_exist(output_path)


def tests_plot_cumulative_series_cpue_by_season():
    result = runner.invoke(cli, ["plot-cumulative-cpue-series-by-season", "--help"])
    assert_command_with_input_and_output_paths(result)

    output_path = "cumulative_by_season.png"
    input_path = "tests/data/esfuerzo_capturas_mensuales_gatos_socorro.csv"
    result = runner.invoke(
        cli,
        [
            "plot-cumulative-cpue-series-by-season",
            "--input-path",
            input_path,
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout
    response = plot_cumulative_cpue_series_by_season(input_path, output_path)
    assert "http://islasgeci.org:100/plot_cumulative_series_cpue_by_season" in response.url

    input_path = "tests/data/feral_goat_aerial_monitoring.csv"
    with pytest.raises(HTTPError):
        plot_cumulative_cpue_series_by_season(input_path, output_path)


def tests_plot_cumulative_series_cpue_by_flight_entrypoint():
    result = runner.invoke(cli, ["plot-cumulative-series-cpue-by-flight", "--help"])
    assert_command_with_input_and_output_paths(result)

    output_path = "cumulative_by_flight.png"
    input_path = "tests/data/feral_goat_capture_effort.csv"
    result = runner.invoke(
        cli,
        [
            "plot-cumulative-series-cpue-by-flight",
            "--input-path",
            input_path,
            "--output-path",
            output_path,
        ],
    )
    assert "200" in result.stdout
    response = plot_cumulative_series_cpue_by_flight(input_path, output_path)
    assert "http://islasgeci.org:100/plot_cumulative_series_cpue_by_flight" in response.url


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


def tests_version():
    obtained_result = get_command_help("version")
    assert_successful_command(obtained_result)
    obtained_result = runner.invoke(cli, ["version"])
    assert "1.0.1" in obtained_result.stdout


def assert_command_with_input_and_output_paths(result):
    assert_successful_command(result)
    assert_input_path_argument(result)
    assert_output_path_argument(result)


def assert_successful_command(result):
    assert result.exit_code == 0


def assert_input_path_argument(results):
    assert "--input-path " in results.stdout
    assert " Path of input data " in results.stdout


def assert_argument(result, option_name, message):
    assert f"--{option_name}" in result.stdout
    assert f" {message} " in result.stdout


def assert_output_path_argument(result, message="Path of figure to write"):
    assert_argument(result, "output-path", message)
