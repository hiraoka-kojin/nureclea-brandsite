#!/usr/bin/env python3
"""
全ブログ記事にSEO・LLMO対応タグを一括追加するスクリプト。
追加内容: OGP / Twitter Card / canonical / JSON-LD (Article + FAQPage)
"""
import json
import re
import os
from pathlib import Path

BASE_URL = "https://nureclea.com"
PUBLIC_DIR = Path(__file__).parent.parent / "public"

with open(PUBLIC_DIR / "articles.json", encoding="utf-8") as f:
    articles_data = json.load(f)

articles_map = {a["file"]: a for a in articles_data}


def strip_tags(html_fragment):
    return re.sub(r"<[^>]+>", "", html_fragment).strip()


def extract_faqs(html):
    faqs = []
    for item in re.findall(r'<div class="faq-item">(.*?)</div>', html, re.DOTALL):
        q = re.search(r'class="faq-question"[^>]*>(.*?)</p>', item, re.DOTALL)
        a = re.search(r'class="faq-answer"[^>]*>(.*?)</p>', item, re.DOTALL)
        if q and a:
            q_text = re.sub(r"^Q[．\.\s]+", "", strip_tags(q.group(1)))
            a_text = re.sub(r"^A[．\.\s]+", "", strip_tags(a.group(1)))
            if q_text and a_text:
                faqs.append({"q": q_text, "a": a_text})
    return faqs


def build_seo_block(title, description, filename, publish_date, category, faqs):
    url = f"{BASE_URL}/{filename}"

    article_schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "datePublished": publish_date,
        "dateModified": publish_date,
        "author": {"@type": "Organization", "name": "ヌレクリア編集部", "url": BASE_URL},
        "publisher": {"@type": "Organization", "name": "ヌレクリア", "url": BASE_URL},
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "articleSection": category,
    }

    lines = [
        "    <!-- SEO / OGP -->",
        f'    <meta property="og:type" content="article">',
        f'    <meta property="og:title" content="{title}">',
        f'    <meta property="og:description" content="{description}">',
        f'    <meta property="og:url" content="{url}">',
        f'    <meta property="og:site_name" content="ヌレクリア">',
        f'    <meta property="og:locale" content="ja_JP">',
        f'    <meta name="twitter:card" content="summary">',
        f'    <meta name="twitter:site" content="@nureclea">',
        f'    <meta name="twitter:title" content="{title}">',
        f'    <meta name="twitter:description" content="{description}">',
        f'    <link rel="canonical" href="{url}">',
        "    <!-- 構造化データ（SEO・LLMO） -->",
        '    <script type="application/ld+json">',
        json.dumps(article_schema, ensure_ascii=False, indent=2),
        "    </script>",
    ]

    if faqs:
        faq_schema = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": faq["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": faq["a"]},
                }
                for faq in faqs
            ],
        }
        lines += [
            '    <script type="application/ld+json">',
            json.dumps(faq_schema, ensure_ascii=False, indent=2),
            "    </script>",
        ]

    return "\n".join(lines)


MARKER = '<link rel="stylesheet" href="style.css">'
processed = skipped = errors = 0

for html_file in sorted(PUBLIC_DIR.glob("blog-*.html")):
    filename = html_file.name
    if filename in ("blog.html", "blog-article-sample.html"):
        continue

    html = html_file.read_text(encoding="utf-8")

    if 'property="og:title"' in html:
        print(f"SKIP (already done): {filename}")
        skipped += 1
        continue

    article = articles_map.get(filename, {})
    publish_date = article.get("publishDate", "2026-04-17")
    category = article.get("category", "フェムケア")

    title_m = re.search(r"<title>(.*?)(?:｜ヌレクリア)?</title>", html)
    desc_m = re.search(r'<meta name="description" content="(.*?)"', html)
    title = title_m.group(1).replace("｜ヌレクリア", "").strip() if title_m else article.get("title", "")
    description = desc_m.group(1) if desc_m else article.get("excerpt", "")

    faqs = extract_faqs(html)
    seo_block = build_seo_block(title, description, filename, publish_date, category, faqs)

    if MARKER in html:
        html = html.replace(MARKER, seo_block + "\n    " + MARKER, 1)
        html_file.write_text(html, encoding="utf-8")
        print(f"OK: {filename}  (FAQ: {len(faqs)}件)")
        processed += 1
    else:
        print(f"ERROR: マーカーが見つかりません: {filename}")
        errors += 1

print(f"\n完了: {processed}件追加 / {skipped}件スキップ / {errors}件エラー")
