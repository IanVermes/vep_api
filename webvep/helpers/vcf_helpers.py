#!/usr/bin/env python3
# -*- coding: utf8 -*-

from importlib.resources import read_text
import re
import typing as t

import vcfpy

_BINOMIAL_PATTERN = re.compile(r"((?:[a-zA-Z]+_[a-zA-Z]+))")


def extract_binomial_name(text: str) -> t.Union[t.Tuple[str, str], None]:
    result = _BINOMIAL_PATTERN.search(text)
    if result:
        raw_name = result.group(0)
        genus, species, *_rest = tuple(raw_name.split("_"))
        return (genus, species)
    else:
        return None


GENOMES = read_text(f"{__package__}", "vep_99_genomes.txt")


def _extract_binomial_names() -> t.Set[t.Tuple[str, str]]:
    names: t.Set[t.Tuple[str, str]] = set()
    for line in GENOMES.splitlines():
        name = extract_binomial_name(line)
        if name:
            names.add(name)
        else:
            continue
    return names


BINOMIAL_NAMES = _extract_binomial_names()


def validate_vcf_content(file: t.TextIO) -> bool:
    try:
        _ = vcfpy.Reader(file)
    except vcfpy.IncorrectVCFFormat:
        outcome = False
    else:
        outcome = True
    return outcome
