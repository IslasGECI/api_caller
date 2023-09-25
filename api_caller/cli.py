import typer

cli = typer.Typer()


@cli.command()
def call(
    service_name: str = typer.Option(help=""),
    port: int = typer.Option(help=""),
    entrypoint_name: str = typer.Option(help=""),
):
    pass
