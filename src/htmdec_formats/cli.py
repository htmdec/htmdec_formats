"""Console script for htmdec_formats."""
import htmdec_formats

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for htmdec_formats."""
    console.print("Replace this message by putting your code into "
               "htmdec_formats.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
