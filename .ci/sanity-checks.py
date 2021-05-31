#!/usr/bin/env python3

import inspect
import re
import sys
import typing as t
from collections import Counter
from enum import Enum
from glob import glob
from textwrap import dedent, wrap


class ExitStatus(Enum):
    SUCCESS = 0
    ERROR = 1


PROGRAM_STATUS = ExitStatus.SUCCESS
RE_URLS = re.compile(r"(?:ftp|https?)://[^\}]*")


def print_description() -> None:
    """
    Print the docstring of the calling function, but at most once.
    """
    frame = inspect.currentframe()

    caller_frame = inspect.getouterframes(frame)[1][0]
    caller_name = inspect.getframeinfo(caller_frame).function
    caller_func = eval(caller_name)
    try:
        if caller_func.warning_already_printed == True:
            return
    except AttributeError:
        caller_func.warning_already_printed = True
        doc = dedent(caller_func.__doc__.strip("\n"))
        # Textwrap cannot really wrap paragraphs correctly.
        # So we first split the text into multiple paragraphs and wrap them individually.
        for paragraph in doc.split("\n\n"):
            for line in wrap(paragraph):
                print(line)
            print()


def check_for_duplicate_urls_in_references(files: t.List[t.AnyStr]) -> None:
    """
    Some references point to the same URL.

    This can happen either because two references share the same URL, in this case consider merging the references.
    Another option is, that the current bibtex style supports both `url` and `note` fields and prints both URLs. Consider removing the `note` field.
    """
    global PROGRAM_STATUS
    for file in files:
        with open(file, "rt") as f:
            content = f.read()

        urls = Counter(map(sanitize_url, RE_URLS.findall(content)))
        for url, count in sorted(urls.items()):
            if count > 1:
                print_description()
                print(f"Duplicate: {url}\n    The URL occurs {count} times.")
                PROGRAM_STATUS = ExitStatus.ERROR


def sanitize_url(url: str) -> str:
    """
    This function strips to the protocol, e.g., http, from urls.

    This ensures that URLs can be compared, even with different protocols, for example, if both http and https are used.
    """
    prefixes = ["https", "http", "ftp"]
    for prefix in prefixes:
        if url.startswith(prefix):
            url = url[len(prefix) :]
    return url


def main() -> None:
    check_for_duplicate_urls_in_references(glob("*.bbl"))

    if PROGRAM_STATUS == ExitStatus.SUCCESS:
        print("All checks passed!")
        sys.exit(0)
    elif PROGRAM_STATUS == ExitStatus.ERROR:
        sys.exit(1)


if __name__ == "__main__":
    main()
