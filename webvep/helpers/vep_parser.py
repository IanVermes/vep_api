from dataclasses import dataclass
import functools
import re

import typing as t

_NA_TOKEN = "-"
_EMPTY_STRING = ""
_LOCATION_RGX_PATTERN = re.compile(r"(\w+):(\w+)(?:-(\w+))?")
# Splits `MotifFeature` -> `Motif Feature`
_TRANSCRIPT_TYPE_RGX_PATTERN = re.compile(r"[A-Z][^A-Z]*")


@dataclass
class Raw:
    meta_data: t.Tuple[str, ...]
    columns_names: t.Tuple[str, ...]
    rows: t.Tuple[t.Tuple[str, ...], ...]


def raw_parser(data: bytes) -> Raw:
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


@functools.lru_cache(maxsize=32)
def parse_location(value: str) -> t.Tuple[str, str, str]:
    if value in {_NA_TOKEN, _EMPTY_STRING}:
        return (_EMPTY_STRING, _EMPTY_STRING, _EMPTY_STRING)
    else:
        match = _LOCATION_RGX_PATTERN.search(value)
        if match:
            chromosome, start, stop, *_rest = match.groups(default=_EMPTY_STRING)
            return chromosome, start, stop
        else:
            return (_EMPTY_STRING, _EMPTY_STRING, _EMPTY_STRING)


def parse_gene(value: str) -> str:
    if value in {_NA_TOKEN, _EMPTY_STRING}:
        return _EMPTY_STRING
    else:
        return value


def parse_transcript(value: str) -> str:
    if value in {_NA_TOKEN, _EMPTY_STRING}:
        return _EMPTY_STRING
    else:
        return value


@functools.lru_cache(maxsize=32)
def parse_transcript_type(value: str) -> str:
    # Check transcript is in formatted map, otherwise
    if value in {_NA_TOKEN, _EMPTY_STRING}:
        return _EMPTY_STRING
    else:
        matched_split_string = _TRANSCRIPT_TYPE_RGX_PATTERN.findall(value)
        if matched_split_string:
            return " ".join(matched_split_string)
        else:
            # This conditional may arise if the regex match doesn't happen but most
            # strings should be splitable.
            return value
