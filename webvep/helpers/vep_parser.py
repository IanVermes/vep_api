from dataclasses import dataclass

import typing as t


@dataclass
class Raw:
    meta_data: t.Tuple[str, ...]
    columns_names: t.Tuple[str, ...]
    rows: t.Tuple[t.Tuple[str, ...], ...]


def raw_parser(data: bytes):
    meta_data = []
    columns = []
    rows = []
    for line in data.splitlines():
        if line.startswith(b"## "):
            meta_data.append(line)
        elif line.startswith(b"#"):
            columns.append(line)
        else:
            rows.append(line)
    # Process meta-data
    meta_data_str = [str(b, encoding="utf8").strip().strip("## ") for b in meta_data]

    # Process columns
    column = columns.pop()
    column_names = column.strip().strip(b"#").split()
    column_names_str = [str(b, encoding="utf8") for b in column_names]

    # Process rows
    rows_str = []
    for row in rows:
        row_elems = str(row, encoding="utf8").strip().split()
        rows_str.append(tuple(row_elems))

    return Raw(
        meta_data=tuple(meta_data_str),
        rows=tuple(rows_str),
        columns_names=tuple(column_names_str),
    )
