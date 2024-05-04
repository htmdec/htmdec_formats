"""Console script for htmdec_formats."""

import htmdec_formats

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for htmdec_formats."""
    console.print(
        "Replace this message by putting your code into " "htmdec_formats.cli.main"
    )
    console.print("See Typer documentation at https://typer.tiangolo.com/")


@app.command()
def nmd_to_csv(nmdfile: str, outfile: str):
    """Convert an NMD file to a CSV file."""
    dataset = htmdec_formats.IndenterDataset.from_filename(nmdfile)
    dataset.to_csv(outfile)


@app.command()
def nmd_test_to_csv(nmdfile: str, outfile: str, test_index: int):
    """Convert a single test from an NMD file to a CSV file."""
    dataset = htmdec_formats.IndenterDataset.from_filename(nmdfile)
    test = dataset.tests[test_index]
    test.to_df().to_csv(outfile, index=False)


@app.command()
def nmd_extract_xml(nmdfile: str, outfile: str):
    """Extract the XML from an NMD file."""
    dataset = htmdec_formats.IndenterDataset.from_filename(nmdfile)
    dataset._xml_tree.write(outfile)


if __name__ == "__main__":
    app()
