from api_caller import construct_entrypoint_url, wrap_arguments
import requests
import typer

cli = typer.Typer()


@cli.command()
def write_csv_probability(
    service_name: str = typer.Option(help=""),
    port: int = typer.Option(help=""),
    entrypoint_name: str = typer.Option(help=""),
    input_path: str = typer.Option(help=""),
    bootstrapping_number: int = typer.Option(help=""),
    output_path: str = typer.Option(help=""),
    window_length: int = typer.Option(help=""),
):
    queries = wrap_arguments(
        input_path=input_path,
        bootstrapping_number=bootstrapping_number,
        ouput_path=output_path,
        window_length=window_length,
    )
    url = construct_entrypoint_url(
        "eradication_progress", 10000, "/write_effort_and_captures_with_probability", queries
    )
    requests(url)
