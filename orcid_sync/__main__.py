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


def process_orcid(orcid, crossref=False):
    """处理 ORCID 作品数据，返回整理后的列表"""
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

            # 解析 ORCID 基础数据
            data = extract_from_work_json(detail.get("work", detail))

            # 如果启用 Crossref，尝试补充信息
            if crossref and data.get("title"):
                cr = try_crossref_fill(data["title"])
                if cr:
                    data = merge_crossref_data(data, cr)

            items.append(data)
            time.sleep(0.2)  # 防止请求过快

    # 按发表日期排序（如果无日期则排在最后）
    return sorted(items, key=lambda x: x.get("publication_date") or "")


def main():
    parser = argparse.ArgumentParser(
        description="Sync ORCID works to mkdocs markdown with card layout"
    )
    parser.add_argument("orcid", help="ORCID iD, e.g. 0000-0002-1825-0097")
    parser.add_argument(
        "--out", default="docs/publications.md", help="Output markdown file"
    )
    parser.add_argument(
        "--crossref",
        action="store_true",
        help="Try to fill missing data using Crossref",
    )
    args = parser.parse_args()

    # 处理数据
    items = process_orcid(args.orcid, crossref=args.crossref)
    md_content = render_markdown(items)

    # 写入文件
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Wrote {args.out}")


if __name__ == "__main__":

    main()
