# GEO-SEO Skill Tools

Tools for the `geo-seo-sys` skill — Generative Engine Optimization.

## Files

- `generate_ai_pages.py` — Main generator. Reads pages.json, produces AI pages, hybrid pages, sitemap, robots.txt
- `nginx-bot-routing.conf` — nginx snippet for dual-serving (bots get semantic HTML, humans get SPA)

## Quick Start

```bash
# Generate AI layer for your site
python3 generate_ai_pages.py /path/to/pages.json /path/to/site/ai/ \
    --site-url https://yoursite.com \
    --site-name "Your Site" \
    --author "Your Name"

# Copy nginx snippet
sudo cp nginx-bot-routing.conf /etc/nginx/snippets/ai-bot-routing.conf
sudo nginx -t && sudo systemctl reload nginx
```

## pages.json Format

```json
{
  "pages": [
    {
      "slug": "my-article",
      "title": "Titolo IT",
      "title_en": "Title EN",
      "description": "Descrizione",
      "description_en": "Description",
      "content": "<p>HTML content IT</p>",
      "content_en": "<p>HTML content EN</p>",
      "category": "article",
      "status": "published",
      "createdAt": "2026-01-01T00:00:00Z",
      "updatedAt": "2026-02-28T00:00:00Z"
    }
  ]
}
```

## What It Generates

| Output | Purpose |
|--------|---------|
| `/ai/{slug}.html` | Pure semantic HTML for self-identifying bot crawlers |
| `/{slug}.html` | Hybrid page (SPA shell + content) for browser-based AI tools |
| `sitemap.xml` | All published URLs with priorities and lastmod |
| `robots.txt` | Explicit Allow for 10+ AI crawler user-agents |
