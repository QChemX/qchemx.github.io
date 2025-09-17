#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WIP
"""

from typing import Any, Optional
from urllib.parse import quote_plus

import requests

HEADERS = {
    "Accept": "application/json",
    "User-Agent": (
        "orcid-mkdocs-sync/2.1 "
        "(https://github.com/yourname/orcid-mkdocs-sync)"
    ),
}

CROSSREF_SEARCH = "https://api.crossref.org/works?query.title={}&rows=1"


def fetch_works(orcid_id: str) -> Any:
    """
    Get a list of works on ORCID.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_work_detail(orcid_id: str, put_code: str) -> Any:
    """
    Get ORCID single article details.
    """
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/work/{put_code}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()


def try_crossref_fill(title: str) -> Optional[dict]:
    """
    Get supplementary information from Crossref,
    such as DOI, publisher, author, etc.
    """
    try:
        q = quote_plus(title)
        r = requests.get(CROSSREF_SEARCH.format(q), timeout=20)
        if r.status_code != 200:
            return None
        data = r.json()
        items = data.get("message", {}).get("items", [])
        if not items:
            return None

        item = items[0]

        # format authors
        authors = []
        for a in item.get("author", []):
            given = a.get("given", "")
            family = a.get("family", "")
            authors.append(f"{given} {family}".strip())

        # published date
        date_parts = item.get("issued", {}).get("date-parts", [[None, None, None]])
        published_date = "-".join(str(x) for x in date_parts[0] if x)

        return {
            "doi": item.get("DOI"),
            "publisher": item.get("publisher"),
            "url": item.get("URL"),
            "authors": authors,
            "publication_date": published_date,
        }
    except Exception:
        return None


if __name__ == "__main__":

    print(__file__)
