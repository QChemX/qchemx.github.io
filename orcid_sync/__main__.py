#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WIP
"""

import argparse
import time

from .api import fetch_work_detail, fetch_works, try_crossref_fill
from .data import extract_from_work_json, merge_crossref_data
from .render import render_markdown

__version__ = "0.2.0"


def process_orcid(orcid: str, crossref: bool = False) -> list:
    """
    Process ORCID work data
    and return a collated list.
    """
    print("Fetching works list...")
    works_json = fetch_works(orcid)
    groups = works_json.get("group", [])

    items = []
    for g in groups:
        summaries = g.get("work-summary", [])
        for s in summaries:
            put_code = s.get("put-code")
            try:
                detail = fetch_work_detail(orcid, put_code)
            except Exception as e:
                print(f"Failed to fetch detail for put-code {put_code}: {e}")
                continue

            # parse ORCID basic data
            data = extract_from_work_json(detail.get("work", detail))

            # If Crossref is enabled,
            # try supplementing the information.
            if crossref and data.get("title"):
                cr = try_crossref_fill(data["title"])
                if cr:
                    data = merge_crossref_data(data, cr)

            items.append(data)
            time.sleep(0.2)  # prevent too fast requests

    # sort by published date
    # in descending order (newest to oldest)
    return sorted(
        items,
        key=lambda x: x.get("publication_date") or "",
        reverse=True
    )


def main() -> None:
    """
    The main function.
    """
    parser = argparse.ArgumentParser(
        prog="orcid_sync",
        description="Sync ORCID works to mkdocs Markdown files.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "orcid",
        nargs="?",
        type=str,
        help="ORCID ID, e.g. 0009-0004-9233-6237"
    )
    parser.add_argument(
        "-o",
        "--out",
        default="docs/publications.md",
        type=str,
        help="The output Markdown file."
    )
    parser.add_argument(
        "-c",
        "--crossref",
        action="store_true",
        help="Try to fill missing data using Crossref."
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Print the version number of %(prog)s and exit.",
        version=f"%(prog)s {__version__}"
    )

    command_args = parser.parse_args()

    # process data
    items = process_orcid(
        command_args.orcid,
        crossref=command_args.crossref
    )
    md_content = render_markdown(items)

    # write to a file
    with open(command_args.out, "w", encoding="utf-8") as file_object:
        file_object.write(md_content)
    print(f"Wrote {command_args.out}")


if __name__ == "__main__":

    main()
