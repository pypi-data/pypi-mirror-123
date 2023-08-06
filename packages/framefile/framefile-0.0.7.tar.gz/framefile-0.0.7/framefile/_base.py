# SPDX-FileCopyrightText: (c) 2021 Artёm IG <github.com/rtmigo>
# SPDX-License-Identifier: MIT

import glob
import os.path
import re
from enum import IntEnum, auto
from functools import lru_cache
from pathlib import Path
from typing import Union, Iterable, Tuple, Callable


class Format(IntEnum):
    percent = auto()
    hash = auto()


class NumbersCountError(ValueError):
    pass


class PatternMismatchError(ValueError):
    pass


def iter_spans(text: str, fmt: Format = Format.hash, min_length: int = 2) \
        -> Iterable[Tuple[int, int, int]]:
    if fmt == Format.hash:
        return iter_hash_spans(text, min_length=min_length)
    if fmt == Format.percent:
        return iter_pct_spans(text, min_length=min_length)
    raise ValueError(fmt)


def is_pattern(text: str, fmt: Format = Format.hash, min_length: int = 2) \
        -> bool:
    for _ in iter_spans(text, fmt=fmt, min_length=min_length):
        return True
    return False


def iter_hash_spans(text: str, min_length: int) \
        -> Iterable[Tuple[int, int, int]]:
    match: re.Match
    for match in re.finditer(r'#+', text, flags=re.MULTILINE):
        s, e = match.span(0)
        if e - s < min_length:
            continue
        yield s, e, e - s


def iter_pct_spans(text: str, min_length: int) \
        -> Iterable[Tuple[int, int, int]]:
    match: re.Match
    for match in re.finditer(r'%(\d+)d', text, flags=re.MULTILINE):
        s, e = match.span(0)
        if e - s < min_length:
            continue
        yield s, e, int(match.group(1))


def hash_pattern_to_regex(pattern: str) -> str:
    return _pattern_to_regex(pattern, iter_func=iter_hash_spans)


def pct_pattern_to_regex(pattern: str) -> str:
    return _pattern_to_regex(pattern, iter_func=iter_pct_spans)



@lru_cache()
def _pattern_to_regex(pattern: str, iter_func: Callable) -> str:
    pattern = pattern.replace("#", "\0")
    result = re.escape(pattern)
    result = result.replace("\0", "#")
    #result = result.replace(r'\#', '#')

    for start, end, digits_count in reversed(
            list(iter_func(result, min_length=1))):
        return (result[:start] +
                "(\\d{" + str(digits_count) + "})" +
                result[end:])
    return result


@lru_cache()
def hash_pattern_to_glob(pattern: str) -> str:
    result = pattern.replace("#", "\0")
    result = glob.escape(result)
    result = result.replace("\0", "#")
    #raise Exception()
    #result = result.replace(r'\#', '#')
    result = result.replace(r'#', '[0-9]')
    return result


def pct_pattern_to_glob(pattern: str) -> str:
    # TODO rewrite with iter_pct_spans to avoid rare errors like img%04d###.png
    return hash_pattern_to_glob(pct_to_hash_pattern(pattern))


def hash_extract_number(pattern: str, text: str) -> int:
    return _extract_number(pattern, text, hash_pattern_to_regex)


def pct_extract_number(pattern: str, text: str) -> int:
    return _extract_number(pattern, text, pct_pattern_to_regex)


def _extract_number(pattern: str, text: str,
                    to_regex_func: Callable[[str], str]) -> int:
    rx = to_regex_func(pattern)
    m = re.match(rx, text, flags=re.MULTILINE)
    if m is None:
        raise PatternMismatchError
    return int(m.group(1))


def iter_digit_spans(text: str, min_length: int) \
        -> Iterable[Tuple[int, int]]:
    match: re.Match
    for match in re.finditer(r'\d+', text, flags=re.MULTILINE):
        s, e = match.span(0)
        if e - s < min_length:
            continue
        yield s, e


def pct_pattern(length: int) -> str:
    return f"%0{length}d"


def hash_pattern(length: int) -> str:
    return "#" * length


def _filename_to_pattern(filename: Union[str, Path],
                         to_pattern_func: Callable,
                         min_length: int) -> str:
    filename = str(filename)
    match: re.Match
    for s, e in reversed(list(
            iter_digit_spans(filename, min_length=min_length))):
        return (filename[:s] +
                to_pattern_func(e - s) +
                filename[e:])

    return filename


@lru_cache()
def pct_to_hash_pattern(pattern: str) -> str:
    def replacer(m: re.Match) -> str:
        return hash_pattern(int(m.group(1)))

    return re.sub(r'%(\d+)d', replacer, pattern, flags=re.MULTILINE)


def filename_to_pct_pattern(filename: Union[str, Path], min_length=2) -> str:
    return _filename_to_pattern(filename,
                                to_pattern_func=pct_pattern,
                                min_length=min_length)


def filename_to_hash_pattern(filename: Union[str, Path], min_length=2) -> str:
    return _filename_to_pattern(filename,
                                to_pattern_func=hash_pattern,
                                min_length=min_length)
