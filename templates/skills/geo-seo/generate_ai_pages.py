#!/usr/bin/env python3
"""
GEO-SEO: AI Page Generator (d-nd-seed skill tool)
==================================================

Generates semantic HTML pages optimized for AI crawlers from a pages.json
content source. Creates three output layers:

  1. /ai/{slug}.html     — Pure semantic HTML for bot-identified crawlers
  2. {slug}.html          — Hybrid pages (SPA shell + full content)
  3. sitemap.xml          — Auto-generated from all published pages
  4. robots.txt           — AI-friendly, welcoming all known crawlers

Usage:
    python3 generate_ai_pages.py <pages.json> <output_dir> [--site-url URL] [--site-name NAME]

Example:
    python3 generate_ai_pages.py /opt/site/data/pages.json /opt/site/ai/ \\
        --site-url https://example.com --site-name "My Site"

The script is idempotent — safe to run on every deploy or content update.

Part of the geo-seo-sys skill from d-nd-seed.
"""

import json
import sys
import os
import re
import argparse
from datetime import datetime, timezone


# ── Configuration (override via CLI args) ────────────────────────────────

SITE_URL = "https://example.com"
SITE_NAME = "My Site"
SITE_DESCRIPTION = "Site description for AI crawlers."
AUTHOR_NAME = "Author Name"

# Category to JSON-LD type mapping — extend for your content types
CATEGORY_SCHEMA = {
    "paper": "ScholarlyArticle",
    "documentation": "TechArticle",
    "article": "Article",
    "thought": "Article",
    "insight": "Article",
    "editorial": "Article",
    "dnd-model": "TechArticle",
    "kernel": "TechArticle",
    "experiment": "TechArticle",
    "tool": "SoftwareApplication",
    "blog": "BlogPosting",
    "product": "Product",
}

# Category to human-readable section name
CATEGORY_SECTION = {
    "paper": "Research Papers",
    "documentation": "Documentation",
    "article": "Articles",
    "thought": "Thoughts",
    "insight": "Insights",
    "editorial": "Editorial",
    "blog": "Blog",
    "tool": "Tools",
}


# ── HTML Cleaning ────────────────────────────────────────────────────────

def clean_html_for_ai(html_content):
    """Strip presentation attributes, keep semantic structure."""
    if not html_content:
        return ""
    html_content = re.sub(r'\s+style="[^"]*"', '', html_content)
    html_content = re.sub(r'\s+class="[^"]*"', '', html_content)
    html_content = re.sub(r'<(div|span|p)>\s*</\1>', '', html_content)
    html_content = re.sub(r'\n{3,}', '\n\n', html_content)
    return html_content.strip()


# ── JSON-LD ──────────────────────────────────────────────────────────────

def generate_jsonld(page, lang="en"):
    """Generate JSON-LD structured data for a page."""
    schema_type = CATEGORY_SCHEMA.get(page.get("category", ""), "Article")
    title = page.get("title_en", page["title"]) if lang == "en" else page["title"]
    description = page.get("description_en", page.get("description", "")) if lang == "en" else page.get("description", "")

    ld = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "headline": title,
        "description": description,
        "url": f"{SITE_URL}/{page['slug']}",
        "inLanguage": lang,
        "publisher": {"@type": "Organization", "name": SITE_NAME.split(" — ")[0] if " — " in SITE_NAME else SITE_NAME, "url": SITE_URL},
        "author": {"@type": "Person", "name": AUTHOR_NAME},
        "datePublished": page.get("createdAt", ""),
        "dateModified": page.get("updatedAt", ""),
    }

    if schema_type == "ScholarlyArticle":
        ld["isPartOf"] = {"@type": "CreativeWorkSeries", "name": f"{SITE_NAME} Research Papers", "url": SITE_URL}

    return json.dumps(ld, ensure_ascii=False, indent=2)


# ── Page Generators ─────────────────────────────────────────────────────

def generate_page_html(page, lang="en"):
    """Generate a pure semantic HTML page for AI crawlers."""
    title = page.get("title_en", page["title"]) if lang == "en" else page["title"]
    description = page.get("description_en", page.get("description", "")) if lang == "en" else page.get("description", "")
    content = page.get("content_en", page.get("content", "")) if lang == "en" else page.get("content", "")
    category = page.get("category", "article")
    section = CATEGORY_SECTION.get(category, "Content")

    content = clean_html_for_ai(content)
    jsonld = generate_jsonld(page, lang)

    citation_meta = ""
    if category == "paper":
        citation_meta = f"""
    <meta name="citation_title" content="{title}">
    <meta name="citation_author" content="{AUTHOR_NAME}">
    <meta name="citation_publication_date" content="{page.get('createdAt', '')[:10]}">
    <meta name="dc.type" content="ScholarlyArticle">"""

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — {SITE_NAME}</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}/{page['slug']}">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:url" content="{SITE_URL}/{page['slug']}">
    <meta property="og:site_name" content="{SITE_NAME}">
    {citation_meta}
    <script type="application/ld+json">
{jsonld}
    </script>
    <style>
        body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.7; color: #1a1a1a; }}
        h1 {{ font-size: 1.8em; }} h2 {{ font-size: 1.4em; margin-top: 1.5em; }}
        blockquote {{ border-left: 3px solid #6366f1; padding-left: 16px; color: #555; font-style: italic; }}
        pre {{ background: #f5f5f5; padding: 16px; border-radius: 4px; overflow-x: auto; }}
        code {{ background: #f0f0f0; padding: 2px 6px; border-radius: 3px; font-size: 0.9em; }}
        nav {{ margin-bottom: 2em; font-size: 0.9em; color: #666; }}
        nav a {{ color: #6366f1; text-decoration: none; }}
        footer {{ margin-top: 3em; padding-top: 1em; border-top: 1px solid #e0e0e0; font-size: 0.85em; color: #888; }}
    </style>
</head>
<body>
    <nav><a href="{SITE_URL}">{SITE_NAME}</a> &rsaquo; {section} &rsaquo; {title}</nav>
    <article>{content}</article>
    <footer>
        <p>&copy; {datetime.now().year} <a href="{SITE_URL}">{SITE_NAME}</a>.</p>
        <p><a href="{SITE_URL}/sitemap.xml">Sitemap</a></p>
    </footer>
</body>
</html>"""


def generate_index_html(pages, lang="en"):
    """Generate an index page listing all published content."""
    groups = {}
    for p in pages:
        section = CATEGORY_SECTION.get(p.get("category", "other"), "Other")
        groups.setdefault(section, []).append(p)

    links = ""
    for section, section_pages in sorted(groups.items()):
        links += f"\n        <h2>{section}</h2>\n        <ul>\n"
        for p in section_pages:
            title = p.get("title_en", p["title"]) if lang == "en" else p["title"]
            desc = p.get("description_en", p.get("description", ""))[:120] if lang == "en" else p.get("description", "")[:120]
            links += f'            <li><a href="{SITE_URL}/{p["slug"]}">{title}</a> — {desc}</li>\n'
        links += "        </ul>\n"

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <title>{SITE_NAME} — All Content</title>
    <meta name="description" content="{SITE_DESCRIPTION}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{SITE_URL}">
    <style>body {{ font-family: system-ui, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6; }}</style>
</head>
<body>
    <h1>{SITE_NAME}</h1>
    <p>{SITE_DESCRIPTION}</p>
    <main>{links}</main>
    <footer><p>&copy; {datetime.now().year} {SITE_NAME}. <a href="{SITE_URL}/sitemap.xml">Sitemap</a></p></footer>
</body>
</html>"""


def generate_sitemap(pages):
    """Generate sitemap.xml with all published pages."""
    priority_map = {"paper": "0.9", "documentation": "0.8", "article": "0.7", "blog": "0.7", "tool": "0.6"}
    urls = [f'  <url>\n    <loc>{SITE_URL}/</loc>\n    <priority>1.0</priority>\n    <changefreq>weekly</changefreq>\n  </url>']
    for p in pages:
        slug = p.get("slug", "")
        if not slug:
            continue
        priority = priority_map.get(p.get("category", ""), "0.5")
        lastmod = p.get("updatedAt", p.get("createdAt", ""))[:10]
        lastmod_tag = f"\n    <lastmod>{lastmod}</lastmod>" if lastmod else ""
        urls.append(f'  <url>\n    <loc>{SITE_URL}/{slug}</loc>\n    <priority>{priority}</priority>\n    <changefreq>monthly</changefreq>{lastmod_tag}\n  </url>')

    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>'


def generate_robots_txt():
    """Generate AI-friendly robots.txt."""
    crawlers = ["GPTBot", "ChatGPT-User", "ClaudeBot", "Claude-Web", "PerplexityBot",
                "Googlebot", "Google-Extended", "Bingbot", "anthropic-ai", "cohere-ai"]
    rules = "\n".join(f"User-agent: {c}\nAllow: /\n" for c in crawlers)
    return f"# AI-friendly robots.txt — generated by geo-seo-sys\n\nUser-agent: *\nAllow: /\n\n{rules}\nSitemap: {SITE_URL}/sitemap.xml\n"


def generate_hybrid_page(page, spa_template, all_pages, lang="en"):
    """Generate hybrid page: SPA shell + full pre-rendered content."""
    title = page.get("title_en", page["title"]) if lang == "en" else page["title"]
    description = page.get("description_en", page.get("description", "")) if lang == "en" else page.get("description", "")
    content = page.get("content_en", page.get("content", "")) if lang == "en" else page.get("content", "")
    category = page.get("category", "article")
    section = CATEGORY_SECTION.get(category, "Content")

    content = clean_html_for_ai(content)
    jsonld = generate_jsonld(page, lang)

    # Related pages
    related = [f'<li><a href="/{p["slug"]}">{p.get("title_en", p["title"]) if lang == "en" else p["title"]}</a></li>'
               for p in all_pages if p.get("slug") != page.get("slug") and p.get("category") == category]
    related_html = f'\n      <nav aria-label="Related content"><h2>Related in {section}</h2><ul>{"".join(related)}</ul></nav>' if related else ""

    html = spa_template
    html = re.sub(r'<title>[^<]*</title>', f'<title>{title} — {SITE_NAME}</title>', html)
    html = re.sub(r'<meta name="description" content="[^"]*"', f'<meta name="description" content="{description}"', html)
    html = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{SITE_URL}/{page["slug"]}"', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*"', f'<meta property="og:title" content="{title}"', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*"', f'<meta property="og:description" content="{description}"', html)
    html = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{SITE_URL}/{page["slug"]}"', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*"', f'<meta name="twitter:title" content="{title}"', html)
    html = re.sub(r'<meta name="twitter:description" content="[^"]*"', f'<meta name="twitter:description" content="{description}"', html)

    html = html.replace('</head>', f'    <script type="application/ld+json">\n{jsonld}\n    </script>\n</head>')

    root_content = f"""
      <nav aria-label="Breadcrumb"><a href="/">{SITE_NAME}</a> &rsaquo; {section} &rsaquo; {title}</nav>
      <article><header><h1>{title}</h1><p><em>{description}</em></p></header>{content}</article>
{related_html}
      <footer><p>&copy; {datetime.now().year} {SITE_NAME}.</p></footer>"""

    marker = '<div id="root">'
    if marker in html:
        start = html.index(marker) + len(marker)
        for end_marker in ['</div>\n    <noscript>', '</div>\n    <div id="admin-root">',
                           '</div>\n  <script', '</div>\n    <script']:
            if end_marker in html[start:]:
                end = html.index(end_marker, start)
                html = html[:start] + root_content + "\n    " + html[end:]
                break

    return html


# ── Main ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="GEO-SEO: AI Page Generator")
    parser.add_argument("pages_json", nargs="?", default="/opt/site/data/pages.json", help="Path to pages.json")
    parser.add_argument("output_dir", nargs="?", default="/opt/site/ai", help="Output directory for AI pages")
    parser.add_argument("--site-url", default=None, help="Site URL (e.g. https://example.com)")
    parser.add_argument("--site-name", default=None, help="Site name")
    parser.add_argument("--site-desc", default=None, help="Site description")
    parser.add_argument("--author", default=None, help="Author name")
    args = parser.parse_args()

    global SITE_URL, SITE_NAME, SITE_DESCRIPTION, AUTHOR_NAME
    if args.site_url: SITE_URL = args.site_url.rstrip("/")
    if args.site_name: SITE_NAME = args.site_name
    if args.site_desc: SITE_DESCRIPTION = args.site_desc
    if args.author: AUTHOR_NAME = args.author

    # Load pages
    with open(args.pages_json, encoding="utf-8") as f:
        data = json.load(f)

    pages = data.get("pages", data if isinstance(data, list) else [])
    published = [p for p in pages if p.get("status") == "published"]
    print(f"[GEO-SEO] Found {len(published)} published pages out of {len(pages)} total")

    os.makedirs(args.output_dir, exist_ok=True)
    site_root = os.path.dirname(args.output_dir)

    # 1. Generate AI pages
    generated = 0
    for page in published:
        slug = page.get("slug", "")
        if not slug:
            continue
        html = generate_page_html(page, lang="en")
        with open(os.path.join(args.output_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        generated += 1
        print(f"  [{page.get('category', '?'):16s}] {slug[:50]:50s} ({len(page.get('content_en', page.get('content', ''))):>7,} chars)")

    # 2. Generate index
    with open(os.path.join(args.output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(generate_index_html(published))

    # 3. Sitemap + robots.txt
    with open(os.path.join(site_root, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(generate_sitemap(published))
    with open(os.path.join(site_root, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(generate_robots_txt())

    # 4. Hybrid pages (if SPA index.html exists)
    hybrid_count = 0
    spa_index = os.path.join(site_root, "index.html")
    if os.path.exists(spa_index):
        with open(spa_index, "r", encoding="utf-8") as f:
            spa_template = f.read()
        for page in published:
            slug = page.get("slug", "")
            if not slug:
                continue
            hybrid = generate_hybrid_page(page, spa_template, published)
            with open(os.path.join(site_root, f"{slug}.html"), "w", encoding="utf-8") as f:
                f.write(hybrid)
            hybrid_count += 1

    print(f"\n[GEO-SEO] Complete:")
    print(f"  AI pages:     {generated}")
    print(f"  Hybrid pages: {hybrid_count}")
    print(f"  Sitemap URLs: {len(published) + 1}")
    print(f"  AI size:      {sum(os.path.getsize(os.path.join(args.output_dir, f)) for f in os.listdir(args.output_dir)):,} bytes")


if __name__ == "__main__":
    main()
