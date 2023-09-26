from api_caller import construct_entrypoint_url, wrap_arguments
import requests
import typer

cli = typer.Typer()


@cli.command()
def write_csv_probability(
    input_path: str = typer.Option(help=""),
    bootstrapping_number: int = typer.Option(help=""),
    output_path: str = typer.Option(help=""),
    window_length: int = typer.Option(help=""),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/write_effort_and_captures_with_probability",
        input_path=input_path,
        bootstrapping_number=bootstrapping_number,
        ouput_path=output_path,
        window_length=window_length,
    )
    response = requests.get(url)
    print(response.status_code)


@cli.command()
def write_probability_progress_figure(
    input_path: str = typer.Option(help=""),
    output_path: str = typer.Option(help=""),
):
    url = construct_entrypoint_url(
        "eradication_progress",
        10000,
        "/write_probability_figure",
        input_path=input_path,
        output_path=output_path,
    )
    response = requests.get(url)
    print(response.status_code)
