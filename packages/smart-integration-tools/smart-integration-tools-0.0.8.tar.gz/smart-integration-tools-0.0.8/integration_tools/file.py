import os
import csv
from io import StringIO
from typing import Union, Generator, List, Optional


def delete_file(filename: str):
    os.remove(filename)


def write_csv_file(
    filename: str,
    data: Union[list, dict, Generator],
    fieldnames: Optional[List[str]] = None,
    delimiter: str = '\t',
    extension: str = '.tsv',
) -> str:
    """Write csv file

    Args:
        filename (str): file path
        data (Union[list, dict, Generator]): data
        fieldnames (Optional[List[str]], optional): file fieldnames. Defaults to None.
        delimiter (str, optional): csv delimiter. Defaults to '\t'.
        extension (str, optional): file extension. Defaults to '.tsv'.

    Returns:
        str: filename
    """
    if extension not in filename:
        filename = f"{filename}{extension}"
    with open(filename, 'w') as f:
        if not fieldnames:
            d = iter(data)
            fieldnames = list(next(d).keys())
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(fieldnames)
        for row in data:
            writer.writerow(row.values())
    return filename


def write_ram_file(
    f: StringIO, data: Union[Generator, list], fieldnames: list, delimiter='\t'
) -> StringIO:
    """Write file from ram

    Args:
        f (StringIO): stringio file content
        data (Union[Generator, list]): data
        fieldnames (list): fieldnames
        delimiter (str, optional): file delimiter. Defaults to '\t'.

    Returns:
        StringIO: stringio file content
    """
    writer = csv.writer(f, delimiter=delimiter)
    writer.writerow(fieldnames)
    for row in data:
        writer.writerow(row.values())
    return f
