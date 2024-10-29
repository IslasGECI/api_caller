from geci_caller import cli

import requests_mock
from typer.testing import CliRunner

runner = CliRunner()


def tests_write_aerial_monitoring():
    result = runner.invoke(cli, ["write-aerial-monitoring", "--help"])
    assert_command_with_input_and_output_paths(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstraps " in result.stdout
    result = runner.invoke(
        cli,
        [
            "write-aerial-monitoring",
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
    result = runner.invoke(cli, ["filter-by-method", "--help"])
    assert_command_with_input_and_output_paths(result)
    assert " Extraction method " in result.stdout

    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/filter_by_method"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "filter-by-method",
                "--input-path",
                "effort_captures.csv",
                "--method",
                "aerea",
                "--output-path",
                "filtered_data.csv",
            ],
        )
        assert m.call_count == 1
        assert "200" in result.stdout


def tests_write_population_status():
    result = runner.invoke(cli, ["write-population-status", "--help"])
    assert_command_with_input_and_output_paths(result)
    assert " Number of bootstraps " in result.stdout

    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/write_population_status"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "write-population-status",
                "--input-path",
                "effort_captures.csv",
                "--bootstrapping-number",
                10,
                "--output-path",
                "population_status.json",
            ],
        )
        assert m.call_count == 1
        assert "200" in result.stdout


def test_call_entrypoint():
    result = runner.invoke(cli, "--help")
    assert_successful_command(result)
    assert "write-probability-progress-figure " in result.stdout

    result = runner.invoke(cli, ["write-csv-probability", "--help"])
    assert_successful_command(result)
    assert_input_path_argument(result)
    assert "--bootstrapping-number " in result.stdout
    assert " Number of bootstrap by window " in result.stdout
    assert "--output-path " in result.stdout
    assert " Path of csv file to write " in result.stdout
    assert "--window-length " in result.stdout
    assert " Number of months by window " in result.stdout

    result = runner.invoke(
        cli, ["write-probability-progress-figure", "--help"])
    assert_command_with_input_and_output_paths(result)

    result = runner.invoke(cli, ["plot-cpue-vs-cum-captures", "--help"])
    assert_command_with_input_and_output_paths(result)

    result = runner.invoke(cli, ["plot-comparative-catch-curves", "--help"])
    assert "--socorro-path " in result.stdout
    assert " Path of Socorro data " in result.stdout
    assert "--guadalupe-path " in result.stdout
    assert " Path of Guadalupe data " in result.stdout
    assert_output_path_argument(result)


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


def tests_write_csv_probability_entrypoint():
    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/write_effort_and_captures_with_probability"
        m.get(entrypoint)
        result = runner.invoke(
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
        assert "200" in result.stdout


def tests_write_probability_figure_entrypoint():
    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/write_probability_figure"
        m.get(entrypoint)
        result = runner.invoke(
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
        assert "200" in result.stdout


def tests_plot_cumulative_series_cpue_by_flight_entrypoint():
    result = runner.invoke(
        cli, ["plot-cumulative-series-cpue-by-flight", "--help"])
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
    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/plot_cpue_vs_cum_captures"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "plot-cpue-vs-cum-captures",
                "--input-path",
                "probabilities.csv",
                "--output-path",
                "figure.png",
            ],
        )
        assert m.call_count == 1
        assert "200" in result.stdout


def tests_plot_custom_cpue_vs_cum_captures_entrypoint():
    result = runner.invoke(
        cli, ["plot-custom-cpue-vs-cum-captures", "--help"])
    assert_command_with_input_and_output_paths(result)
    assert " Path of config file " in result.stdout

    with requests_mock.Mocker() as m:
        entrypoint = "http://eradication_progress:10000/plot_custom_cpue_vs_cum_captures"
        m.get(entrypoint)
        result = runner.invoke(
            cli,
            [
                "plot-custom-cpue-vs-cum-captures",
                "--input-path",
                "goat_data.csv",
                "--config-path",
                "config.json",
                "--output-path",
                "figure.png",
            ],
        )
        assert result.exit_code == 0
        assert "200" in result.stdout


def tests_plot_comparative_catch_curves():
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
