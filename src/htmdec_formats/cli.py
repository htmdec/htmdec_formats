"""Console script for htmdec_formats."""

import htmdec_formats

import typer
from rich.console import Console
from typing import Optional
from typing_extensions import Annotated

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


@app.command()
def pxt_describe(pxtfile: str):
    """Describe the contents of a PXT file."""
    dataset = htmdec_formats.ARPESDataset.from_file(pxtfile)
    console.print()
    for line in dataset._metadata.splitlines():
        console.print(line)
    console.print()
    console.print("[bold]Sections:[/bold]")
    for section in dataset.metadata.sections():
        console.print(section)
    console.print()
    console.print("[bold]Bounds:[/bold]")
    console.print(dataset.bounds)
    console.print()
    console.print("[bold]Data shape:[/bold]")
    console.print(dataset.array_data.shape)


@app.command()
def pxt_info_export(pxtfile: str, outfile: str):
    """Export the metadata of a PXT file to a file."""
    dataset = htmdec_formats.ARPESDataset.from_file(pxtfile)
    with open(outfile, "w") as f:
        l = f.write(dataset._metadata)
        console.print(f"Output {l} bytes to {outfile}.")


@app.command()
def pxt_info_query(
    pxtfile: str, section: str, key: Annotated[Optional[str], typer.Argument()] = None
):
    """Query the metadata of a PXT file."""
    dataset = htmdec_formats.ARPESDataset.from_file(pxtfile)
    if section not in dataset.metadata:
        console.print(f"Section {section} not found.")
        return
    if key is not None:
        if key not in dataset.metadata[section]:
            console.print(f"Key {key} not found in section {section}.")
            return
        console.print(
            f"[bold]{section} -> {key}[/bold]: {dataset.metadata[section][key]}"
        )
    else:
        console.print(f"[bold]{section}[/bold]:")
        for key in dataset.metadata[section]:
            console.print(f"  {key}: {dataset.metadata[section][key]}")


@app.command()
def pxt_to_hdf5(pxtfile: str, outfile: str):
    """Convert a PXT file to an HDF5 file."""
    dataset = htmdec_formats.ARPESDataset.from_file(pxtfile)
    dataset.to_hdf5(outfile)


if __name__ == "__main__":
    app()
