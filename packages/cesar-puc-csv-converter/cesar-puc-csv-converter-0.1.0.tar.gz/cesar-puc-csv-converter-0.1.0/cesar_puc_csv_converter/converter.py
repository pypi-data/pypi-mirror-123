import logging
from pathlib import Path
from typing import Any, Tuple

import pandas as pd


logger = logging.getLogger(__name__)


def read_csv_file(source: Path, delimiter: str) -> Tuple[Any, ...]:
    """Load csv files from disk.

    Args:
        source (Path): Path of a single csv file or a directory containing csv files.
        delimiter (str): Separator for columns in csv.

    Return:
        tuple: tuple of DataFrames.
    """
    if source.is_file():
        logger.info("Reading single file %s", source)
        return (
            pd.read_csv(
                filepath_or_buffer=source, delimiter=delimiter, index_col=False
            ),
        )

    logger.info("Reading all files within subdirectory %s", source)
    data = tuple(
        [
            pd.read_csv(
                filepath_or_buffer=name, delimiter=delimiter, index_col=False
            )
            for name in source.iterdir()
        ]
    )
    return data


def save_to_json_files(
    csvs: Tuple[Any, ...], output_path: Path, prefix: str = 'file'
) -> None:
    """Save dataframes to Disk.

    Args:
        csvs (tuple): Tuple with dataframes that will be converted
        output_path (Path): Path where to save the json files
        file_names (str): Name of files. If nothing is given it will
    """
    i = 0
    while i < len(csvs):
        file_name = f"{prefix}_{i}.json"
        logger.info("Saving file %s in folder %s", file_name, output_path)

        data: pd.DataFrame = csvs[i]
        data.to_json(
            path_or_buf=output_path.joinpath(file_name),
            orient="records",
            indent=4,
        )
        i += 1
