from os.path import join
from pathlib import Path
from tempfile import TemporaryDirectory

from pandas import DataFrame

from cesar_puc_csv_converter.converter import read_csv_file, save_to_json_files


def test_should_read_file_run_read_csv_file(
    example_dataset: DataFrame,
) -> None:
    with TemporaryDirectory() as tmpdirname:
        path_file = join(tmpdirname, 'example-file.csv')
        example_dataset.to_csv(path_file)

        results = read_csv_file(
            source=Path(path_file),
            delimiter=',',
        )
        assert isinstance(results, tuple)
        assert isinstance(results[0], DataFrame)


def test_should_read_path_run_read_csv_file(
    example_dataset: DataFrame,
) -> None:
    with TemporaryDirectory() as tmpdirname:
        example_dataset.to_csv(join(tmpdirname, 'example-file.csv'))

        results = read_csv_file(
            source=Path(tmpdirname),
            delimiter=',',
        )
        assert isinstance(results, tuple)
        assert isinstance(results[0], DataFrame)


def test_should_save_to_json_files(example_dataset: DataFrame) -> None:
    with TemporaryDirectory() as tmpdirname:
        save_to_json_files(
            csvs=(example_dataset,),
            output_path=Path(tmpdirname),
        )

        p = Path(tmpdirname)
        results = list(p.glob('*.json'))
        assert len(results) == 1
