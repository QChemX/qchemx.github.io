#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WIP
"""

from typing import Any


def extract_from_work_json(work_json: Any) -> dict:
    """
    Parse the work JSON returned by ORCID
    and extract basic information.
    """
    title = work_json.get("title", {}).get("title", {}).get("value", "No title")
    abstract = work_json.get("short-description") or ""

    # DOI
    doi = None
    for ext in work_json.get("external-ids", {}).get("external-id", []):
        if ext.get("external-id-type", "").lower() == "doi":
            doi = ext.get("external-id-value")
            if doi and doi.lower().startswith("doi:"):
                doi = doi.split(":", 1)[1]
            break

    # URL
    url = (
        work_json.get("url", {}).get("value")
        if work_json.get("url")
        else None
    )

    # journal
    journal = None
    if isinstance(work_json.get("journal-title"), dict):
        journal = work_json["journal-title"].get("value")
    else:
        journal = work_json.get("journal-title")

    # published date
    publication_date = None
    if "publication-date" in work_json:
        date_parts = [
            work_json["publication-date"].get(k, {}).get("value")
            for k in ["year", "month", "day"]
            if work_json["publication-date"].get(k)
        ]
        publication_date = "-".join(date_parts)

    return {
        "title": title,
        "abstract": abstract,
        "doi": doi,
        "url": url,
        "journal": journal,
        "publication_date": publication_date,
        "authors": [],
        "publisher": None,
        "citation_link": f"https://doi.org/{doi}" if doi else None,
    }


def merge_crossref_data(orcid_data: dict, crossref_data: dict) -> dict:
    """
    Merge ORCID and Crossref data.
    """
    for key in ["doi", "publisher", "url", "authors", "publication_date"]:
        if crossref_data.get(key):
            orcid_data[key] = crossref_data[key]
    return orcid_data


if __name__ == "__main__":

    print(__file__)
