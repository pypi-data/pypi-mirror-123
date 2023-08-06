import logging
from pathlib import Path

import click

from .converter import read_csv_file, save_to_json_files


logging.basicConfig(
    level="DEBUG",
    format="'%(asctime)s - %(name)s - %(levelname)s - %(message)s'",
)
logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--input",
    "-i",
    default="./",
    help="Path where the files will be loaded for conversion.",
    type=str,
)
@click.option(
    "--output",
    "-o",
    default="./",
    help="Path where the converted files will be saved.",
    type=str,
)
@click.option(
    "--delimiter",
    "-d",
    default=",",
    help="Separator used to split the files.",
    type=str,
)
@click.option(
    "--prefix",
    "-p",
    prompt=True,
    prompt_required=False,
    default="file",
    help=(
        "Prefix used to prepend to the name of the converted file saved on disk."
        " The suffix will be a number starting from 0. ge: file_0.json."
    ),
)
def converter(
    input: str = "./",
    output: str = "./",
    delimiter: str = ",",
    prefix: str = 'file',
) -> None:
    """Convert Single file or list of CSV files to json."""

    input_path = Path(input)
    output_path = Path(output)
    logger.info(f"Input path {input_path}")
    logger.info(f"Output path {output_path}")

    for p in [input_path, output_path]:
        if not (p.is_file() or p.is_dir()):
            raise TypeError(f"Not a valid path or file name. {p}")

    data = read_csv_file(source=input_path, delimiter=delimiter)
    save_to_json_files(data, output_path, prefix)

    logger.info("Finishing processing")
