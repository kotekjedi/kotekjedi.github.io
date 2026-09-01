from __future__ import annotations

import json
import re
from collections import OrderedDict
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
    "nickname": "Sasha",
    "tagline": "AI safety, adversarial ML & LLM red-teaming",
    "location": "ELLIS Institute Tübingen / MPI-IS",
    "email": "kotekjedi@gmail.com",
    "cv": "assets/pdf/cv.pdf",
    "photo": "assets/img/profile_mine_new.jpg",
    "photo_caption": "Tübingen, Germany",
    "highlight_name": "Alexander Panfilov",
    "bio": [
        "I am a third-year ELLIS / IMPRS-IS PhD student in Tübingen, advised by Jonas Geiping and Maksym Andriushchenko. I did MATS 9.0 as part of Google DeepMind stream.",
        "I work on AI safety, particularly on red-teaming LLMs and stuff around them. Roughly two days a week I am an AI doomer.",
        "My research has been covered by <a href=\"https://www.wired.com/story/a-new-trick-reveals-ai-models-inner-thoughts/\" target=\"_blank\" rel=\"noopener\">press</a> and <a href=\"https://simonwillison.net/2026/Aug/11/stealing-reasoning-traces/\" target=\"_blank\" rel=\"noopener\">blogs</a>, and has affected <a href=\"https://support.claude.com/en/articles/16761192-preserved-thinking-changing-how-the-messages-api-handles-thinking-blocks-to-protect-against-distillation\" target=\"_blank\" rel=\"noopener\">frontier model deployments</a>.",
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
    <a href="https://scholar.google.com/citations?user=9hlJ9W0AAAAJ&hl=en" target="_blank">Felix Dangel</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=gzRuY4cAAAAJ" target="_blank">Valentyn Boreiko</a>,
    <a href="https://scholar.google.com/citations?user=0ZAb3tsAAAAJ&hl=en" target="_blank">Matthias Hein</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=exaNV-0AAAAJ" target="_blank">Shashwat Goel</a>,
    <a href="https://scholar.google.com/citations?hl=en&user=e-YbZyEAAAAJ" target="_blank">Illia Shumailov</a>,
    <a href="https://scholar.google.com/citations?user=ZNtuJYoAAAAJ" target="_blank">Maksym Andriushchenko</a>, and
    <a href="https://scholar.google.de/citations?user=206vNCEAAAAJ&hl=en" target="_blank">Jonas Geiping</a>.
    """
).strip()

NAV_LINKS = [
    {"label": "research", "href": "#featured"},
    {"label": "news", "href": "#news"},
    {"label": "talks", "href": "#talks"},
    {"label": "cv", "href": "assets/pdf/cv.pdf"},
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

CONFERENCE_HIGHLIGHT_CLASS = "highlight highlight-conference"

ARTEFACT_LABELS = {
    "url": "paper",
    "html": "website",
    "code": "code",
    "poster": "poster",
}


def slugify(value: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return clean or "entry"


def highlight_oral(text: str) -> str:
    return re.sub(
        r"\b(oral)\b", r'<span class="pen-circle">\1</span>', text, flags=re.IGNORECASE
    )


def highlight_conferences(text: str) -> str:
    def repl(match: re.Match) -> str:
        return f'<span class="{CONFERENCE_HIGHLIGHT_CLASS}">{match.group(1)}</span>'

    result = text
    for conf in CONFERENCES:
        pattern = r"\b(" + re.escape(conf) + r"(?:\s+\d{4})?)\b"
        result = re.sub(pattern, repl, result, flags=re.IGNORECASE)
    return result


def load_dated_json(path: Path) -> List[Dict[str, object]]:
    with path.open("r", encoding="utf-8") as fh:
        items = json.load(fh)
    for item in items:
        item["date_obj"] = datetime.strptime(item["date"], "%Y-%m-%d")
    return sorted(items, key=lambda itm: itm["date_obj"], reverse=True)


def render_news_html(news_items: List[Dict[str, object]]) -> str:
    groups: "OrderedDict[int, List[Dict[str, object]]]" = OrderedDict()
    for item in news_items:
        groups.setdefault(item["date_obj"].year, []).append(item)

    rendered_groups = []
    for year, items in groups.items():
        entries = []
        for item in items:
            date_label = item["date_obj"].strftime("%b %d")
            text = highlight_oral(highlight_conferences(item["text"]))
            entries.append(
                f'<li class="news-item"><span class="news-date">{date_label}</span>'
                f'<div class="news-body">{text}</div></li>'
            )
        entries_html = "\n".join(entries)
        rendered_groups.append(
            dedent(
                f"""
                <div class="news-year-group">
                    <h3 class="year-label" aria-label="{year}">{year}</h3>
                    <ul class="news-list">
                        {entries_html}
                    </ul>
                </div>
                """
            ).strip()
        )
    groups_html = "\n".join(rendered_groups)
    return f'<div class="news-groups scrollable">\n{groups_html}\n</div>'


def render_talks_html(talks: List[Dict[str, object]]) -> str:
    groups: "OrderedDict[int, List[Dict[str, object]]]" = OrderedDict()
    for talk in talks:
        groups.setdefault(talk["date_obj"].year, []).append(talk)

    rendered_groups = []
    for year, items in groups.items():
        rows_html = "\n".join(render_talk_item(talk) for talk in items)
        rendered_groups.append(
            dedent(
                f"""
                <div class="talk-year-group">
                    <h3 class="year-label" aria-label="{year}">{year}</h3>
                    <ul class="talk-list">
                        {rows_html}
                    </ul>
                </div>
                """
            ).strip()
        )
    groups_html = "\n".join(rendered_groups)
    return f'<div class="talk-groups scrollable">\n{groups_html}\n</div>'


def render_talk_item(talk: Dict[str, object]) -> str:
    date_label = talk["date_obj"].strftime("%b %d")
    title = talk.get("title")
    venue = talk["venue"]
    event = talk.get("event")
    event_url = talk.get("event_url")
    talk_type = talk.get("type", "talk")

    lead = venue
    badge = ""

    sub_parts = []
    if talk_type not in ("talk",):
        sub_parts.append(talk_type)
    if title:
        sub_parts.append(f"<em>{title}</em>")
    sub = " · ".join(sub_parts)
    if event:
        sub = f"{sub} ({event})" if sub else f"({event})"
    sub_html = f'<p class="talk-sub">{sub}</p>' if sub else ""

    links = []
    if event_url:
        links.append(
            f'<a class="pill-button ghost" href="{event_url}" target="_blank" rel="noopener">event</a>'
        )
    if slides := talk.get("slides"):
        links.append(
            f'<a class="pill-button ghost" href="{slides}" target="_blank" rel="noopener">slides</a>'
        )
    if video := talk.get("video"):
        links.append(
            f'<a class="pill-button ghost" href="{video}" target="_blank" rel="noopener">video</a>'
        )
    links_html = (
        f'<div class="talk-links">{" ".join(links)}</div>' if links else ""
    )

    return dedent(
        f"""
        <li class="talk-item">
            <span class="talk-date">{date_label}</span>
            <div class="talk-body">
                <p class="talk-lead">{lead}{badge}</p>
                {sub_html}
            </div>
            {links_html}
        </li>
        """
    ).strip()


def load_press_map(path: Path = ROOT / "press.json") -> Dict[str, List[Dict[str, str]]]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def is_featured(entry) -> bool:
    return entry.fields.get("featured", "").strip().lower() in ("true", "1", "yes")


def render_press_rows(press_links: List[Dict[str, str]]) -> str:
    rows = []
    for item in press_links:
        label = f'<span class="press-outlet">{item["outlet"]}</span>'
        if item.get("title"):
            label += f' &mdash; {item["title"]}'
        if item.get("url"):
            rows.append(
                f'<li><a href="{item["url"]}" target="_blank" rel="noopener">{label}</a></li>'
            )
        else:
            rows.append(f"<li>{label}</li>")
    return '<ul class="press-links">\n' + "\n".join(rows) + "\n</ul>"


def render_featured_html(bib_data, press_map: Dict[str, List[Dict[str, str]]]) -> str:
    cards = []
    panels = []
    for entry_key, entry in bib_data.entries.items():
        if not is_featured(entry):
            continue
        slug = slugify(entry_key)
        title = entry.fields.get("title", "Untitled")
        booktitle_raw = entry.fields.get("booktitle", "Preprint")
        display_text = entry.fields.get("display", booktitle_raw)
        venue_html = highlight_conferences(f'<span class="venue">{display_text}</span>')
        url = entry.fields.get("url", "#")
        img = entry.fields.get("img", "assets/img/publications/placeholder.png")
        actions = format_artefact_links(entry)
        press_links = press_map.get(entry_key, [])
        if press_links:
            actions += (
                f'\n<button class="pill-button ghost" data-toggle-target="featured-press-{slug}">press</button>'
            )
            panels.append(
                f'<div class="toggle-panel toggle-panel-press" id="featured-press-{slug}">\n'
                f"{render_press_rows(press_links)}\n</div>"
            )
        cards.append(
            dedent(
                f"""
                <div class="featured-card">
                    <a class="featured-thumb" href="{url}" target="_blank" rel="noopener"><img src="{img}" alt="{title} figure" loading="lazy"></a>
                    <span class="featured-meta">{venue_html}</span>
                    <a class="featured-title" href="{url}" target="_blank" rel="noopener">{title}</a>
                    <div class="featured-actions">{actions}</div>
                </div>
                """
            ).strip()
        )
    cards_html = "\n".join(cards)
    panels_html = "\n".join(panels)
    return f'<div class="featured-grid">\n{cards_html}\n</div>\n{panels_html}'


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
    return f'<span class="pen-circle">{label.strip().lower()}</span>'


def format_artefact_links(entry) -> str:
    links = []
    for field, label in ARTEFACT_LABELS.items():
        url = entry.fields.get(field)
        if url:
            links.append(
                f'<a class="pill-button" href="{url}" target="_blank" rel="noopener">{label}</a>'
            )
    return "\n".join(links)


def format_publication(entry_key: str, entry, press_map: Dict[str, List[Dict[str, str]]]) -> str:
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
    drop_fields = ("img", "code", "html", "poster", "presentation", "abstract", "featured", "display", "press")
    cleaned_lines = []
    for line in bibtex_raw.splitlines():
        stripped = line.strip()
        if any(stripped.startswith(f"{field} =") for field in drop_fields):
            continue
        cleaned_lines.append(line)
    bibtex_clean = "\n".join(cleaned_lines).strip()
    bibtex_html = escape(bibtex_clean)

    venue_html = highlight_conferences(f'<span class="venue">{display_text}</span>')
    year_fragment = (
        f'<span class="pub-year">{year}</span>' if (year and is_preprint) else ""
    )

    parts = [
        '<article class="publication-card">',
        '  <div class="pub-body">',
        f"    <div class=\"pub-meta\">{venue_html}{year_fragment}{badge}</div>",
        f'    <h4 class="pub-title"><a href="{entry.fields.get("url", "#")}" target="_blank" rel="noopener">{title}</a></h4>',
        f'    <p class="pub-authors">{authors}</p>',
        f'    <div class="pub-actions">{artefacts}',
    ]

    press_links = press_map.get(entry_key, [])

    toggle_buttons = []
    if abstract_text:
        toggle_buttons.append(
            f'<button class="pill-button ghost" data-toggle-target="abstract-{slug}">abstract</button>'
        )
    toggle_buttons.append(
        f'<button class="pill-button ghost" data-toggle-target="bibtex-{slug}">bibtex</button>'
    )
    if press_links:
        toggle_buttons.append(
            f'<button class="pill-button ghost" data-toggle-target="press-{slug}">press</button>'
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

    if press_links:
        parts.append(
            f'<div class="toggle-panel toggle-panel-press" id="press-{slug}">\n'
            f"{render_press_rows(press_links)}\n</div>"
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


def build_publications_html(press_map: Dict[str, List[Dict[str, str]]]):
    parser = bibtex.Parser()
    bib_data = parser.parse_file(str(ROOT / "publication_list.bib"))
    cards = [
        format_publication(entry_key, entry, press_map)
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
            f'<a class="social-link" href="{link["url"]}" target="_blank" rel="noopener">{icon_html}<span>{link["label"].lower()}</span></a>'
        )
    return "\n".join(items)


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
    return (
        '<nav class="site-nav">'
        '<a class="brand" href="#top">kotekjedi<span class="brand-cat" aria-hidden="true"> =^..^=</span></a>'
        f'<div class="nav-links">{links}</div></nav>'
    )


def section_heading(cmd: str, title: str, description: Optional[str] = None) -> str:
    desc_html = f'<p class="section-description">{description}</p>' if description else ""
    return (
        '<div class="section-heading">'
        f'<h2 class="section-cmd" id="{cmd}-title" aria-label="{title}">'
        f'<span class="cmd-slash" aria-hidden="true">/</span>{cmd}</h2>'
        f"{desc_html}</div>"
    )


def get_index_html() -> str:
    press_map = load_press_map()
    publications_html, bib_data = build_publications_html(press_map)
    featured_html = render_featured_html(bib_data, press_map)

    featured_section = dedent(
        f"""
        <section class="section" id="featured" aria-labelledby="featured-research-title">
            {section_heading("featured-research", "Featured research")}
            {featured_html}
        </section>
        """
    ).strip()

    # Full publications list is temporarily hidden — uncomment to restore it.
    research_section = ""
    # research_section = dedent(
    #     f"""
    #     <section class="section" id="research" aria-labelledby="research-title">
    #         {section_heading("research", "Research")}
    #         <div class="publications">
    #             {publications_html}
    #         </div>
    #     </section>
    #     """
    # ).strip()

    news_html = render_news_html(load_dated_json(ROOT / "news.json"))
    talks_html = render_talks_html(load_dated_json(ROOT / "talks.json"))
    social_html = build_social_html()
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
            <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
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
                        <h1 class="hero-title">Yo, I&rsquo;m <span class="squiggle">{PERSON["nickname"]}</span>!</h1>
                        <div class="social-row">
                            {social_html}
                        </div>
                        {bio_html}
                        <div class="cta-row">
                            <a class="pill-button primary" href="{PERSON["cv"]}" target="_blank" rel="noopener">cv</a>
                            <a class="pill-button secondary" href="mailto:{PERSON["email"]}">email me</a>
                        </div>
                    </div>
                    <figure class="hero-photo">
                        <img src="{PERSON["photo"]}" alt="{PERSON["first_name"]} {PERSON["last_name"]}" loading="lazy">
                        <figcaption>{PERSON["photo_caption"]}</figcaption>
                    </figure>
                </div>
            </header>

            <main>
                {featured_section}
                <section class="section" id="news" aria-labelledby="news-title">
                    {section_heading("news", "News")}
                    {news_html}
                </section>

                <section class="section" id="talks" aria-labelledby="invited-talks-title">
                    {section_heading("invited-talks", "Invited talks")}
                    {talks_html}
                </section>

                {research_section}
                <section class="section" id="thanks" aria-labelledby="thanks-title">
                    {section_heading("thanks", "Acknowledgements")}
                    <p class="acknowledgement">{ACKNOWLEDGEMENT}</p>
                </section>
            </main>

            <footer class="site-footer">
                <p class="footer-cat" aria-hidden="true">=^..^=</p>
                <p>Vibe-coded with Claude Code. Last updated {datetime.now().strftime("%b %d, %Y")}.</p>
            </footer>
            </div>

            <script>
            const PANEL_PREFIXES = ['abstract-', 'bibtex-', 'press-'];
            document.querySelectorAll('[data-toggle-target]').forEach((button) => {{
                button.addEventListener('click', () => {{
                    const targetId = button.dataset.toggleTarget;
                    const target = document.getElementById(targetId);
                    if (!target) return;
                    target.classList.toggle('is-visible');
                    const expanded = target.classList.contains('is-visible');
                    button.setAttribute('aria-expanded', expanded);

                    const prefix = PANEL_PREFIXES.find((p) => targetId.startsWith(p));
                    if (!prefix || !expanded) return;
                    PANEL_PREFIXES.filter((p) => p !== prefix).forEach((other) => {{
                        const siblingId = targetId.replace(prefix, other);
                        const siblingPanel = document.getElementById(siblingId);
                        if (siblingPanel && siblingPanel.classList.contains('is-visible')) {{
                            siblingPanel.classList.remove('is-visible');
                            const siblingButton = document.querySelector(`[data-toggle-target="${{siblingId}}"]`);
                            if (siblingButton) {{
                                siblingButton.setAttribute('aria-expanded', 'false');
                            }}
                        }}
                    }});
                }});
            }});

            document.querySelectorAll('[data-goto-target]').forEach((button) => {{
                button.addEventListener('click', () => {{
                    const targetId = button.dataset.gotoTarget;
                    const panel = document.getElementById(targetId);
                    if (!panel) return;
                    if (!panel.classList.contains('is-visible')) {{
                        const opener = document.querySelector(`[data-toggle-target="${{targetId}}"]`);
                        if (opener) {{
                            opener.click();
                        }} else {{
                            panel.classList.add('is-visible');
                        }}
                    }}
                    panel.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                }});
            }});
            </script>
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
