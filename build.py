from __future__ import annotations

import json
import re
from datetime import datetime
from html import escape
from pathlib import Path
from textwrap import dedent
from typing import Dict, List, Optional

from pybtex.database import BibliographyData
from pybtex.database.input import bibtex

ROOT = Path(__file__).parent.resolve()
GOOGLE_ANALYTICS_ID = "G-4SLC5348B5"

PERSON = {
    "first_name": "Alexander",
    "last_name": "Panfilov",
    "tagline": "AI safety, Adversarial ML, & LLM Red-Teaming",
    "location": "ELLIS Institute / IMPRS-IS, Tuebingen",
    "email": "kotekjedi@gmail.com",
    "cv": "assets/pdf/cv.pdf",
    "photo": "assets/img/profile_mine_new.jpg",
    "highlight_name": "Alexander Panfilov",
    "bio": [
        "Yo! My name is Sasha and I am a second-year ELLIS / IMPRS-IS PhD student in Tuebingen advised by Jonas Geiping and Maksym Andriushchenko.",
        "I work on AI Safety, particularly on red-teaming LLMs and stuff around them. Roughly two days a week I am an AI doomer.",
        "Previously I was obsessed with LLM jailbreaks, trying to understand realistic threat models, whether current safety evaluations are trustworthy, and whether we’re doomed. Lately I’m leaning into white-box alignment methods and AI control.",
        "I am open to collaboration - feel free to drop an email! I’m also looking for a safety/security internship opportunity in 2026/2027.",
    ],
}

SOCIAL_LINKS = [
    {
        "label": "Scholar",
        "url": "https://scholar.google.com/citations?user=M65_TPEAAAAJ&hl=en",
        "icon_img": "assets/icons8-google-scholar.svg",
    },
    {
        "label": "Twitter",
        "url": "https://x.com/kotekjedi_ml",
        "icon": "fa-brands fa-x-twitter",
    },
    {
        "label": "LinkedIn",
        "url": "https://www.linkedin.com/in/kotekjedi",
        "icon": "fab fa-linkedin",
    },
    {
        "label": "GitHub",
        "url": "https://github.com/kotekjedi",
        "icon": "fab fa-github",
    },
    {
        "label": "Email",
        "url": "mailto:kotekjedi@gmail.com",
        "icon": "fa-solid fa-envelope",
    },
]

FOCUS_AREAS = [
    {
        "title": "Research Interests",
        "body": "I find introspection capability of LLMs fascinating and think it can be used as a way to reason about white-box interventions and useful for self-jailbreaking.",
    },
    {
        "title": "Whereabouts",
        "body": "Based in London from January through March for MATS. Happy to grab a coffee if you are around!",
    },
    {
        "title": "Plans",
        "body": "Planning to attend ICLR 2026 in Brazil. Happy to catch up there!",
    },
]

ACKNOWLEDGEMENT = dedent(
    """
    I am grateful to the many friends and colleagues, from whom I learned so much, for their invaluable guidance
    and for shaping my research vision. I would like to especially acknowledge
    <a href="https://www.linkedin.com/in/svyatoslav-oreshin/" target="_blank">Svyatoslav Oreshin</a>,
    <a href="https://scholar.google.com/citations?user=wcdrgdYAAAAJ&hl=en" target="_blank">Arip Asadualev</a>,
    <a href="https://scholar.google.de/citations?user=4jdISHwAAAAJ&hl=en" target="_blank">Roland Zimmermann</a>,
    <a href="https://scholar.google.com/citations?user=aeCiRSYAAAAJ&hl=en" target="_blank">Thaddaeus Wiedemer</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=jgPzOmgAAAAJ" target="_blank">Jack Brady</a>,
    <a href="https://scholar.google.com/citations?user=v-JL-hsAAAAJ&hl=en" target="_blank">Wieland Brendel</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=gzRuY4cAAAAJ" target="_blank">Valentyn Boreiko</a>,
    <a href="https://scholar.google.com/citations?user=0ZAb3tsAAAAJ&hl=en" target="_blank">Matthias Hein</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=exaNV-0AAAAJ" target="_blank">Shashwat Goel</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=e-YbZyEAAAAJ" target="_blank">Illia Shumailov</a>,
    <a href="https://scholar.google.com/citations?user=ZNtuJYoAAAAJ" target="_blank">Maksym Andriushchenko</a>, and
    <a href="https://scholar.google.de/citations?user=206vNCEAAAAJ&hl=en" target="_blank">Jonas Geiping</a>.
    """
).strip()

NAV_LINKS = [
    {"label": "News", "href": "#news"},
    {"label": "Research", "href": "#research"},
]

CONFERENCES = [
    "ICML",
    "ICLR",
    "NeurIPS",
    "NIPS",
    "CoLLAs",
    "TMLR",
    "CVPR",
    "ICCV",
    "ECCV",
    "AAAI",
    "IJCAI",
    "ACL",
    "EMNLP",
    "NAACL",
]

ARTEFACT_LABELS = {
    "url": "Paper",
    "html": "Website",
    "code": "Code",
    "poster": "Poster",
}


def slugify(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return clean or "entry"


def highlight_oral(text: str) -> str:
    return re.sub(r"\b(oral)\b", r"<strong>\1</strong>", text, flags=re.IGNORECASE)


def highlight_conferences(text: str) -> str:
    result = text
    for conf in CONFERENCES:
        pattern = r"\b(" + re.escape(conf) + r"(?:\s+\d{4})?)\b"
        result = re.sub(pattern, r"<strong>\1</strong>", result, flags=re.IGNORECASE)
    return result


def load_news(path: Path = ROOT / "news.json") -> List[Dict[str, object]]:
    with path.open("r", encoding="utf-8") as fh:
        news_items = json.load(fh)
    for item in news_items:
        item["date_obj"] = datetime.strptime(item["date"], "%Y-%m-%d")
    return sorted(news_items, key=lambda itm: itm["date_obj"], reverse=True)


def render_news_items(news_items: List[Dict[str, object]]) -> str:
    rendered = []
    for item in news_items:
        date_label = item["date_obj"].strftime("%b %d, %Y")
        text = highlight_oral(highlight_conferences(item["text"]))
        rendered.append(
            dedent(
                f"""
                <li class="news-item">
                    <span class="news-date">{date_label}</span>
                    <div class="news-body">{text}</div>
                </li>
                """
            ).strip()
        )
    return "\n".join(rendered)


def format_authors(persons) -> str:
    names = []
    for person in persons:
        first = " ".join(person.get_part("first"))
        last = " ".join(person.get_part("last"))
        full = " ".join(p for p in [first, last] if p).strip()
        if PERSON["highlight_name"] in full:
            full = f'<span class="author-self">{full}</span>'
        names.append(full or "Anonymous")
    return ", ".join(names)


def format_badge(label: Optional[str]) -> str:
    if not label:
        return ""
    variant = label.strip().lower()
    extra_class = " badge-oral" if variant == "oral" else ""
    return f'<span class="badge-pill{extra_class}">{label}</span>'


def format_artefact_links(entry) -> str:
    links = []
    for field, label in ARTEFACT_LABELS.items():
        url = entry.fields.get(field)
        if url:
            links.append(
                f'<a class="pill-button" href="{url}" target="_blank" rel="noopener">{label}</a>'
            )
    return "\n".join(links)


def format_publication(entry_key: str, entry) -> str:
    slug = slugify(entry_key)
    title = entry.fields.get("title", "Untitled")
    booktitle_raw = entry.fields.get("booktitle", "Preprint")
    display_text = entry.fields.get("display", booktitle_raw)
    is_preprint = booktitle_raw.strip().lower() == "preprint"
    year = entry.fields.get("year")
    badge = format_badge(entry.fields.get("presentation"))
    authors = format_authors(entry.persons.get("author", []))
    artefacts = format_artefact_links(entry)
    abstract_text = entry.fields.get("abstract")

    bibliograpy = BibliographyData(entries={entry_key: entry})
    bibtex_raw = bibliograpy.to_string("bibtex").strip()
    drop_fields = ("img", "code", "html", "poster", "presentation", "abstract")
    cleaned_lines = []
    for line in bibtex_raw.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(f"{field} =") for field in drop_fields):
            continue
        cleaned_lines.append(line)
    bibtex_clean = "\n".join(cleaned_lines).strip()
    bibtex_html = escape(bibtex_clean)

    thumb_button = ""
    if abstract_text:
        thumb_button = f'<button class="pill-button thumb-button" data-toggle-target="abstract-{slug}">Abstract</button>'

    venue_html = highlight_oral(
        highlight_conferences(f'<span class="venue">{display_text}</span>')
    )
    year_fragment = f" | {year}" if (year and is_preprint) else ""

    parts = [
        '<article class="publication-card">',
        '  <div class="pub-thumb">',
        f'    <img src="{entry.fields.get("img", "assets/img/publications/placeholder.png")}" alt="{title} cover" loading="lazy">',
    ]
    if thumb_button:
        parts.append(f'    {thumb_button}')
    parts.append("  </div>")
    parts.extend([
        '  <div class="pub-body">',
        f'    <div class="pub-meta">{venue_html}{year_fragment}{badge}</div>',
        f'    <h4 class="pub-title"><a href="{entry.fields.get("url", "#")}" target="_blank" rel="noopener">{title}</a></h4>',
        f'    <p class="pub-authors">{authors}</p>',
        f'    <div class="pub-actions">{artefacts}',
    ])

    toggle_buttons = []
    toggle_buttons.append(
        f'<button class="pill-button ghost" data-toggle-target="bibtex-{slug}">BibTeX</button>'
    )

    parts.append("      " + " ".join(toggle_buttons))
    parts.append("    </div>")

    if abstract_text:
        parts.append(
            dedent(
                f"""
                <div class="toggle-panel" id="abstract-{slug}">
                    <p>{abstract_text}</p>
                </div>
                """
            ).strip()
        )

    parts.append(
        dedent(
            f"""
            <div class="toggle-panel toggle-panel-bib" id="bibtex-{slug}">
                <pre class="pub-bibtex"><code>{bibtex_html}</code></pre>
            </div>
            """
        ).strip()
    )

    parts.append("  </div>")
    parts.append("</article>")
    return "\n".join(parts)


def build_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file(str(ROOT / "publication_list.bib"))
    cards = [
        format_publication(entry_key, entry)
        for entry_key, entry in bib_data.entries.items()
    ]
    return "\n".join(cards), bib_data


def build_social_html() -> str:
    items = []
    for link in SOCIAL_LINKS:
        if icon_src := link.get("icon_img"):
            icon_html = f'<img src="{icon_src}" alt="{link["label"]} icon" loading="lazy">'
        else:
            icon_html = f'<i class="{link["icon"]}"></i>'
        items.append(
            f'<a class="social-link" href="{link["url"]}" target="_blank" rel="noopener">{icon_html}<span>{link["label"]}</span></a>'
        )
    return "\n".join(items)


def build_focus_html() -> str:
    return "\n".join(
        [
            dedent(
                f"""
                <div class="focus-card">
                    <h4>{item["title"]}</h4>
                    <p>{item["body"]}</p>
                </div>
                """
            ).strip()
            for item in FOCUS_AREAS
        ]
    )


def build_structured_data(bib_data) -> str:
    publications = []
    for entry_key, entry in bib_data.entries.items():
        authors = []
        for person in entry.persons.get("author", []):
            first = " ".join(person.get_part("first"))
            last = " ".join(person.get_part("last"))
            authors.append({"@type": "Person", "name": " ".join([first, last]).strip()})
        publication = {
            "@type": "ScholarlyArticle",
            "headline": entry.fields.get("title", ""),
            "author": authors,
            "publisher": {"@type": "Organization", "name": entry.fields.get("booktitle", "")},
        }
        if year := entry.fields.get("year"):
            publication["datePublished"] = year
        if url := entry.fields.get("url"):
            publication["url"] = url
        publications.append(publication)

    data = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": f'{PERSON["first_name"]} {PERSON["last_name"]}',
        "jobTitle": "PhD Student",
        "description": PERSON["tagline"],
        "affiliation": {
            "@type": "Organization",
        "name": "ELLIS Institute Tuebingen",
            "alternateName": "IMPRS-IS",
        },
        "url": "https://kotekjedi.github.io",
        "image": f'https://kotekjedi.github.io/{PERSON["photo"]}',
        "sameAs": [link["url"] for link in SOCIAL_LINKS if link["url"].startswith("http")],
        "email": PERSON["email"],
        "workLocation": {"@type": "Place", "name": "Tuebingen, Germany"},
        "publication": publications,
    }
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_nav_html() -> str:
    links = "".join(
        [f'<a href="{item["href"]}">{item["label"]}</a>' for item in NAV_LINKS]
    )
    return f'<nav class="site-nav"><div class="brand">Sasha&apos;s Website</div><div class="nav-links">{links}</div></nav>'


def get_index_html() -> str:
    publications_html, bib_data = build_publications_html()
    news_html = render_news_items(load_news())
    social_html = build_social_html()
    focus_html = build_focus_html()
    structured_data = build_structured_data(bib_data)
    nav_html = build_nav_html()

    bio_html = "\n".join([f"<p>{paragraph}</p>" for paragraph in PERSON["bio"]])
    analytics_snippet = ""
    if GOOGLE_ANALYTICS_ID:
        analytics_snippet = dedent(
            f"""
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={GOOGLE_ANALYTICS_ID}"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());
              gtag('config', '{GOOGLE_ANALYTICS_ID}');
            </script>
            <script data-goatcounter="https://kotekjedi.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
            """
        ).strip()
    return dedent(
        f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>{PERSON["first_name"]} {PERSON["last_name"]}</title>
            <meta name="description" content="{PERSON["tagline"]}">
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
            <link rel="stylesheet" href="assets/styles.css">
            <link rel="icon" type="image/x-icon" href="assets/favicon_mine.ico">
            {analytics_snippet}
            <script type="application/ld+json">
{structured_data}
            </script>
        </head>
        <body>
            <div class="page-shell">
            {nav_html}
            <header class="hero" id="top">
                <div class="hero-grid">
                    <div class="hero-content">
                        <p class="eyebrow">{PERSON["location"]}</p>
                        <h1>{PERSON["first_name"]} <span>{PERSON["last_name"]}</span></h1>
                        <p class="tagline">{PERSON["tagline"]}</p>
                        <div class="social-row">
                            {social_html}
                        </div>
                        {bio_html}
                        <div class="cta-row">
                            <a class="pill-button primary" href="{PERSON["cv"]}" target="_blank" rel="noopener">Download CV</a>
                            <a class="pill-button secondary" href="mailto:{PERSON["email"]}">Email me</a>
                        </div>
                    </div>
                    <div class="hero-photo">
                        <img src="{PERSON["photo"]}" alt="{PERSON["first_name"]} {PERSON["last_name"]}" loading="lazy">
                    </div>
                </div>
            </header>

            <main>
                <section class="panel focus-panel" aria-labelledby="focus-title">
                    <div class="panel-heading">
                        <h2 id="focus-title">My current...</h2>
                    </div>
                    <div class="focus-grid">
                        {focus_html}
                    </div>
                </section>

                <section class="panel news-panel" id="news" aria-labelledby="news-title">
                    <div class="panel-heading">
                        <h2 id="news-title">News & updates</h2>
                    </div>
                    <ul class="news-timeline">
                        {news_html}
                    </ul>
                </section>

                <section class="panel" id="research" aria-labelledby="research-title">
                    <div class="panel-heading">
                        <h2 id="research-title">Research</h2>
                        <p class="panel-description">Some of my recent work :) </p>
                    </div>
                    <div class="publications">
                        {publications_html}
                    </div>
                </section>

                <section class="panel" id="contact">
                    <div class="panel-heading">
                        <h3 class="panel-title-sm">Acknowledgements</h3>
                    </div>
                    <p>{ACKNOWLEDGEMENT}</p>
                </section>
            </main>

            <footer class="site-footer">
                <p>Vibe-coded with CodeX. Last updated {datetime.now().strftime("%b %d, %Y")}.</p>
            </footer>
            </div>

            <script>
            document.querySelectorAll('[data-toggle-target]').forEach((button) => {{
                button.addEventListener('click', () => {{
                    const targetId = button.dataset.toggleTarget;
                    const target = document.getElementById(targetId);
                    if (!target) return;
                    target.classList.toggle('is-visible');
                    const expanded = target.classList.contains('is-visible');
                    button.setAttribute('aria-expanded', expanded);

                    const isBibtex = targetId.startsWith('bibtex-');
                    const isAbstract = targetId.startsWith('abstract-');
                    const siblingPrefix = isBibtex ? 'abstract-' : isAbstract ? 'bibtex-' : null;

                    if (siblingPrefix) {{
                        const siblingId = targetId.replace(isBibtex ? 'bibtex-' : 'abstract-', siblingPrefix);
                        const siblingPanel = document.getElementById(siblingId);
                        if (siblingPanel && siblingPanel.classList.contains('is-visible')) {{
                            siblingPanel.classList.remove('is-visible');
                            const siblingButton = document.querySelector(`[data-toggle-target="${{siblingId}}"]`);
                            if (siblingButton) {{
                                siblingButton.setAttribute('aria-expanded', 'false');
                            }}
                        }}
                    }}
                }});
            }});
            </script>
            <script data-goatcounter="https://kotekjedi.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
        </body>
        </html>
        """
    ).strip()


def write_index_html(filename: str = "index.html") -> None:
    html = get_index_html()
    with open(filename, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"Wrote {filename}")


if __name__ == "__main__":
    write_index_html("index.html")
