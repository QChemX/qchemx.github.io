#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
WIP
"""


def render_markdown(items):
    """生成卡片布局的 Markdown 文档"""
    md = [
        "# Publications\n\n",
        "This page was generated automatically.\n\n",
    ]

    for it in items:
        authors = ", ".join(it.get("authors", [])) if it.get("authors") else "Unknown"
        md.append("---\n")  # 卡片分隔线
        md.append(f"### {it['title']}\n")
        md.append(f"**Authors:** {authors}  \n")
        if it.get("journal"):
            md.append(f"**Journal:** {it['journal']}  \n")
        if it.get("publication_date"):
            md.append(f"**Published Date:** {it['publication_date']}  \n")
        if it.get("doi"):
            md.append(f"**DOI:** [{it['doi']}](https://doi.org/{it['doi']})  \n")
        if it.get("citation_link"):
            md.append(
                f"**Citation Link:** [{it['citation_link']}]({it['citation_link']})  \n"
            )
        if it.get("abstract"):
            md.append(f"\n**Abstract:** {it['abstract']}\n")
        md.append("\n")  # 卡片底部空行

    return "\n".join(md)
