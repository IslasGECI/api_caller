import geci_caller as gc
import json
import pandas as pd
import requests
import typer
import io
import logging

logging.basicConfig(level=logging.DEBUG)

cli = typer.Typer()


@cli.command()
def write_posterior_results(
    input_path: str = typer.Option(help="Path of input data"),
    initial_parameters_path: str = typer.Option(help="Path of initial parameters"),
    output_path: str = typer.Option(help="Path of output file"),
):
    url = "http://islasgeci.org:200/write_eradication_bayesian_model_results"
    data_file_like = read_file_as_buffer(input_path)
    initial_parameters_file_like = read_file_as_buffer(initial_parameters_path)
    files = {
        "data_path": (input_path, data_file_like, "application/json"),
        "initial_parameters_path": (
            initial_parameters_path,
            initial_parameters_file_like,
            "application/json",
        ),
    }
    response = requests.post(url, files=files)
    response.raise_for_status()
    json_data = response.json()
    df = pd.DataFrame(json_data)
    df.to_csv(output_path, index=False)
    return response


@cli.command()
def plot_cumulative_cpue_series_by_season(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/plot_cumulative_series_cpue_by_season"
    effort_file_like = read_file_as_buffer(input_path)
    files = {
        "file": (input_path, effort_file_like, "text/csv"),
    }
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    response.raise_for_status()
    print(response.status_code)
    return response


@cli.command()
def plot_cumulative_series_cpue_by_flight(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/plot_cumulative_series_cpue_by_flight"
    input_file_like = read_file_as_buffer(input_path)
    files = {
        "file": (input_path, input_file_like, "text/csv"),
    }
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def write_bootstrap_progress_intervals(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstraps"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    entrypoint_name = "/write_bootstrap_progress_intervals_json"
    url = f"http://islasgeci.org:100{entrypoint_name}"
    input_file_like = read_file_as_buffer(input_path)
    files = {
        "input_path": (input_path, input_file_like, "text/csv"),
    }
    data = {"bootstrapping_number": bootstrapping_number}
    response = requests.post(url, files=files, data=data)
    with open(output_path, "w") as out_file:
        json.dump(response.json(), out_file, indent=2)
    print(response.status_code)
    return response


@cli.command()
def filter_by_method(
    input_path: str = typer.Option(help="Path of input data"),
    method: str = typer.Option(help="Extraction method"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/filter_by_method"
    input_file_like = read_file_as_buffer(input_path)
    files = {
        "input_path": (input_path, input_file_like, "text/csv"),
    }
    data = {"method": method}
    response = requests.post(url, files=files, data=data)
    print(response.status_code)
    response.raise_for_status()
    content = response.json()
    df = pd.DataFrame(content)
    df.to_csv(output_path, index=False)


@cli.command()
def write_aerial_monitoring(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstraps"),
    output_path: str = typer.Option(help="Path of figure to write"),
):

    url = "http://islasgeci.org:100/write_aerial_monitoring"
    input_file_like = read_file_as_buffer(input_path)
    files = {
        "input_path": (input_path, input_file_like, "text/csv"),
    }
    data = {"bootstrapping_number": bootstrapping_number}
    response = requests.post(url, files=files, data=data)
    with open(output_path, "w") as out_file:
        json.dump(response.json(), out_file, indent=2)
    print(response.status_code)
    return response


@cli.command()
def write_population_status_from_mixed_methods(
    first_method_status: str = typer.Option(),
    second_method_status: str = typer.Option(),
    output_path: str = typer.Option(),
):
    url = "http://islasgeci.org:100/write_population_status_from_mixed_methods"
    first_method_file_like = read_file_as_buffer(first_method_status)
    second_method_file_like = read_file_as_buffer(second_method_status)
    files = {
        "first_method_status": (first_method_status, first_method_file_like, "application/json"),
        "second_method_status": (second_method_status, second_method_file_like, "application/json"),
    }
    response = requests.post(url, files=files)
    print(response.status_code)
    with open(output_path, "w") as out_file:
        json.dump(response.json(), out_file, indent=2)


@cli.command()
def plot_comparative_yearly_cpue(
    socorro_path: str = typer.Option(help="Path of Socorro data"),
    guadalupe_path: str = typer.Option(help="Path of Guadalupe data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/plot_comparative_yearly_cpue"
    socorro_file_like = read_file_as_buffer(socorro_path)
    guadalupe_file_like = read_file_as_buffer(guadalupe_path)
    files = {
        "socorro_file": (socorro_path, socorro_file_like, "text/csv"),
        "guadalupe_file": (guadalupe_path, guadalupe_file_like, "text/csv"),
    }
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def plot_comparative_catch_curves(
    socorro_path: str = typer.Option(help="Path of Socorro data"),
    guadalupe_path: str = typer.Option(help="Path of Guadalupe data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/plot_comparative_catch_curves"
    socorro_file_like = read_file_as_buffer(socorro_path)
    guadalupe_file_like = read_file_as_buffer(guadalupe_path)
    files = {
        "socorro_file": (socorro_path, socorro_file_like, "text/csv"),
        "guadalupe_file": (guadalupe_path, guadalupe_file_like, "text/csv"),
    }
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def write_population_status(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstraps"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    entrypoint_name = "/write_population_status"
    url = f"http://islasgeci.org:100{entrypoint_name}"
    with open(input_path, "rb") as f:
        response = requests.post(
            url,
            files={"file": f},
            data={"bootstrapping_number": bootstrapping_number},
        )
    response.raise_for_status()
    with open(output_path, "w") as out_file:
        json.dump(response.json(), out_file, indent=2)


@cli.command()
def write_instantaneous_and_cumulative_cpue(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path to write"),
    resolution: str = typer.Option(default=None, help="Temporal resolution: monthly, season"),
):
    entrypoint_name = "/compute_instantaneous_and_cumulative_cpue"
    url = f"http://islasgeci.org:100{entrypoint_name}"
    data = {
        "resolution": resolution,
    }
    file_like = read_file_as_buffer(input_path)
    response = requests.post(
        url,
        files={"input_path": (input_path, file_like, "text/csv")},
        data=data,
        stream=True,
        timeout=600,
    )
    response.raise_for_status()
    json_data = response.json()
    df = pd.DataFrame(json_data)
    df.to_csv(output_path, index=False)
    return response


@cli.command()
def write_csv_probability(
    input_path: str = typer.Option(help="Path of input data"),
    bootstrapping_number: int = typer.Option(help="Number of bootstrap by window"),
    output_path: str = typer.Option(help="Path of csv file to write"),
    window_length: int = typer.Option(help="Number of months by window"),
    resolution: int = typer.Option(default=None, help="Temporal resolution"),
):
    entrypoint_name = "/write_effort_and_captures_with_probability"
    url = f"http://islasgeci.org:100{entrypoint_name}"
    data = {
        "bootstrapping_number": bootstrapping_number,
        "window_length": window_length,
        "resolution": resolution,
    }
    file_like = read_file_as_buffer(input_path)
    response = requests.post(
        url,
        files={"file": (input_path, file_like, "text/csv")},
        data=data,
        stream=True,
        timeout=600,
    )
    response.raise_for_status()
    json_data = response.json()
    df = pd.DataFrame(json_data)
    df.to_csv(output_path, index=False)
    return response


@cli.command()
def write_probability_progress_figure(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/write_probability_figure"
    file_like = read_file_as_buffer(input_path)
    files = {"file": (input_path, file_like, "text/csv")}
    response = requests.post(url, files=files)
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def plot_custom_cpue_vs_cum_captures(
    input_path: str = typer.Option(help="Path of input data"),
    config_path: str = typer.Option(help="Path of config file"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/plot_custom_cpue_vs_cum_captures"
    file_like = read_file_as_buffer(input_path)
    config_like = read_file_as_buffer(config_path)
    files = {
        "file": (input_path, file_like, "text/csv"),
        "config": (config_path, config_like, "application/json"),
    }
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def plot_cpue_vs_cum_captures(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    extension = output_path.split(".")[-1]
    url = "http://islasgeci.org:100/plot_cpue_vs_cum_captures"
    file_like = read_file_as_buffer(input_path)
    files = {"file": (input_path, file_like, "text/csv")}
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def write_instantaneous_and_cumulative_cpue_time_series_plot(
    input_path: str = typer.Option(help="Path of input data"),
    output_path: str = typer.Option(help="Path of figure to write"),
):
    url = "http://islasgeci.org:100/write_instantaneous_and_cumulative_cpue_time_series_plot"
    input_file_like = read_file_as_buffer(input_path)
    files = {"file": (input_path, input_file_like, "text/csv")}
    extension = output_path.split(".")[-1]
    response = requests.post(url, files=files, data={"format": extension})
    write_response_content(output_path, response)
    print(response.status_code)
    return response


@cli.command()
def version():
    version = gc.__version__
    print(version)


def read_file_as_buffer(file_path):
    with open(file_path, "rb") as file:
        buffer_file = io.BytesIO(file.read())
    return buffer_file


def write_response_content(output_path, response):
    with open(output_path, "wb") as out_file:
        out_file.write(response.content)
