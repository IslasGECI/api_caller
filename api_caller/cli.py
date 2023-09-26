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
    pass
