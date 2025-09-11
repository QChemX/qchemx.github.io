#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WIP
"""

from urllib.parse import quote_plus

import requests

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "orcid-mkdocs-sync/2.1 (https://github.com/yourname/orcid-mkdocs-sync)",
}

CROSSREF_SEARCH = "https://api.crossref.org/works?query.title={}&rows=1"


def fetch_works(orcid_id):
    """获取 ORCID 上的作品列表"""
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_work_detail(orcid_id, put_code):
    """获取 ORCID 单篇作品详情"""
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/work/{put_code}"
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return r.json()


def try_crossref_fill(title):
    """从 Crossref 获取补充信息，如 DOI、出版社、作者等"""
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

        # 格式化作者
        authors = []
        for a in item.get("author", []):
            given = a.get("given", "")
            family = a.get("family", "")
            authors.append(f"{given} {family}".strip())

        # 发表日期
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
