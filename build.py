import json
import time
from datetime import datetime
import re

from pybtex.database.input import bibtex


def get_personal_data():
    name = ["Alexander", "Panfilov"]
    full_name_en = f"{name[0]} {name[1]}"
    full_name_ru = "Александр Панфилов"
    twitter = "kotekjedi_ml"
    github = "kotekjedi"
    linkedin = "kotekjedi"
    cv = "assets/pdf/cv.pdf"

    icons_html = f"""
    <div class="d-flex justify-content-center align-items-center" style="flex-wrap: wrap;">
        <a href="https://scholar.google.com/citations?user=M65_TPEAAAAJ&hl=en" target="_blank" class="m-2"><img src="assets/icons8-google-scholar.svg" alt="Google Scholar" width="36" height="36"></a>
        <a href="https://www.linkedin.com/in/{linkedin}" target="_blank" class="m-2" style="color: black;"><i class="fab fa-linkedin fa-2x"></i></a>
        <a href="https://x.com/{twitter}" target="_blank" class="m-2" style="color: black;"><i class="fa-brands fa-x-twitter fa-2x"></i></a>
        <a href="https://github.com/{github}" target="_blank" class="m-2" style="color: black;"><i class="fab fa-github fa-2x"></i></a>
        <a href="mailto:kotekjedi@gmail.com" class="m-2" style="color: black;"><i class="fa-solid fa-envelope fa-2x"></i></a>

    </div>
    """

    bio_text = f"""
        <img src="assets/img/profile_mine_new.jpg" alt="{full_name_en} ({full_name_ru}) - PhD Student in AI Safety and Machine Learning Security" class="profile-pic img-fluid float-md-right mr-md-3 mb-3">

        <p style="font-size: 1.15em;">
            Yo! My name is <span style="font-weight: 500;">Sasha</span>
  and I am a first-year ELLIS / IMPRS-IS PhD student, based in Tübingen. I find myself very lucky to be advised by<a href="https://jonasgeiping.github.io/" class="m-2" style="font-weight: 500;" target="_blank">Jonas Geiping</a>and<a href="https://www.andriushchenko.me/" class="m-2" style="font-weight: 500;" target="_blank">Maksym Andriushchenko</a>.
        </p>
        <p style="font-size: 1.15em;">
    Broadly, I am interested in adversarial robustness, AI safety, and ML security. In practical terms, I enjoy finding various ways to break machine learning systems. Roughly three days a week I am an AI doomer.
        </p>
    
    <p style="font-size: 1.15em;">
    Lately, I have been focusing on jailbreaking attacks on LLMs, contemplating:
(1) What are the viable threat models for attacks on safety tuning? (2) Are safety jailbreaks truly effective, or are we victims of flawed (LLM-based) evaluations? (3) Are we doomed?
        </p>
        <p style="font-size: 1.15em;">
        You can find my <a href="{cv}" target="_blank" style="text-decoration: none; color: inherit; font-weight: bold; background-color: rgb(255, 255, 179);">CV here</a>. I am always open to collaboration — feel free to reach out via email!</p>
        
        <!-- Hidden SEO content for name variants -->
        <div style="position: absolute; left: -9999px; opacity: 0; pointer-events: none;" aria-hidden="true">
            <span>{full_name_en} {full_name_ru} Alexander Panfilov Александр Панфилов Sasha Panfilov AI Safety Machine Learning Security Adversarial Robustness LLM Jailbreaking PhD Student ELLIS IMPRS-IS Tübingen Research Max Planck Institute for Intelligent Systems MPI-IS Тольятти Togliatti Togliatty Toliatty Samara Самара ITMO ИТМО ITMO University Red Teaming AI Alignment ML Security Research</span>
        </div>
    """
    current_date = time.strftime("%d/%m/%Y")
    footer = f"""
    <footer style="text-align: right; padding: 10px; margin-top: 20px;">
        <p style="font-size: 0.9em;">
            Updated on {current_date}. Website design credits to <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">Michael Niemeyer</a>.
        </p>
    </footer>
    """

    return name, icons_html, bio_text, footer, full_name_en, full_name_ru

def get_acknowledgements():
    s = """
    <div class="row" style="margin-top: 3em;">
        <div class="col-sm-12">
            <h4 style="margin-bottom: 0.5em; font-weight: medium;">Acknowledgements</h4>
            <p style="font-size: 1.15em;">
                I am grateful to the many colleagues I worked with in the past, from whom I learned so much, for their invaluable contributions to my career.
                I would like to especially acknowledge the mentorship and guidance of
                <a href="https://www.linkedin.com/in/svyatoslav-oreshin/" target="_blank">Svyatoslav Oreshin</a>,
                <a href="https://scholar.google.com/citations?user=wcdrgdYAAAAJ&hl=en" target="_blank">Arip Asadualev</a>,
                <a href="https://scholar.google.de/citations?user=4jdISHwAAAAJ&hl=en" target="_blank">Roland Zimmerman</a>,
                <a href="https://scholar.google.com/citations?user=aeCiRSYAAAAJ&hl=en" target="_blank">Thaddaus Wiedemer</a>,
                <a href="https://scholar.google.com/citations?hl=en&user=jgPzOmgAAAAJ" target="_blank">Jack Brady</a>, 
                <a href="https://scholar.google.com/citations?user=v-JL-hsAAAAJ&hl=en" target="_blank">Wieland Brendel</a>,
                <a href="https://scholar.google.com/citations?hl=en&user=gzRuY4cAAAAJ" target="_blank">Valentyn Boreiko</a> and
                <a href="https://scholar.google.com/citations?user=0ZAb3tsAAAAJ&hl=en" target="_blank">Matthias Hein</a>.
            </p>
        </div>
    </div>
    """
    return s

def get_author_dict():
    return {
        # Заполните при необходимости
    }


def generate_person_html(
    persons,
    connection=", ",
    make_bold=True,
    make_bold_name="Alexander Panfilov",
    add_links=True,
):
    links = get_author_dict() if add_links else {}
    s = ""
    for p in persons:
        first_names = " ".join(p.get_part("first"))
        last_names = " ".join(p.get_part("last"))
        full_name = f"{first_names} {last_names}"
        string_part_i = full_name
        if string_part_i in links.keys():
            string_part_i = (
                f'<a href="{links[string_part_i]}" target="_blank">{string_part_i}</a>'
            )
        if make_bold and make_bold_name in full_name:
            string_part_i = f'<span style="font-weight: bold; background-color: rgb(255, 255, 179);">{full_name}</span>'
        if p != persons[-1]:
            string_part_i += connection
        s += string_part_i
    return s


def highlight_oral_text(text):
    """Highlight the word 'oral' in bold only, case-insensitive"""
    # Use regex to find 'oral' (case-insensitive) and wrap it with bold styling
    pattern = r'\b(oral)\b'
    replacement = r'<strong>\1</strong>'
    return re.sub(pattern, replacement, text, flags=re.IGNORECASE)


def highlight_conference_names(text):
    """Highlight major conference names and years in bold"""
    # List of major conferences to highlight
    conferences = ['ICML', 'ICLR', 'NeurIPS', 'NIPS', 'CVPR', 'ICCV', 'ECCV', 'AAAI', 'IJCAI', 'ACL', 'EMNLP', 'NAACL']
    
    for conf in conferences:
        # Match conference name followed by optional space and year (e.g., "ICML 2025", "ICLR", etc.)
        pattern = r'\b(' + re.escape(conf) + r'(?:\s+\d{4})?)\b'
        replacement = r'<strong>\1</strong>'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def generate_presentation_badge(presentation_type):
    """Generate a colored badge for presentation type"""
    if not presentation_type:
        return ""
    
    presentation_type = presentation_type.lower().strip()
    
    # Define badge styles for different presentation types
    badge_styles = {
        'oral': {
            'color': 'rgb(200, 162, 255)',  # Same purple as oral text highlighting
            'text_color': 'white'
        },
        'spotlight': {
            'color': 'rgb(255, 165, 0)',  # Orange
            'text_color': 'white'
        },
        'poster': {
            'color': 'rgb(108, 117, 125)',  # Gray
            'text_color': 'white'
        },
        'workshop': {
            'color': 'rgb(40, 167, 69)',  # Green
            'text_color': 'white'
        }
    }
    
    # Get style or default to blue
    style = badge_styles.get(presentation_type, {
        'color': 'rgb(37, 110, 255)',  # Blue (same as article links)
        'text_color': 'white'
    })
    
    badge_html = f'''<span style="
        background-color: {style['color']}; 
        color: {style['text_color']}; 
        font-size: 0.75em; 
        font-weight: bold; 
        padding: 3px 8px; 
        border-radius: 12px; 
        margin-right: 8px;
        text-transform: uppercase;
        display: inline-block;
    ">{presentation_type}</span>'''
    
    return badge_html


def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;" > <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid" alt="Project image">"""
    s += """</div><div class="col-sm-9" style="font-size: 1.05em;">"""

    # Add presentation badge if available
    badge = ""
    if 'presentation' in entry.fields:
        badge = generate_presentation_badge(entry.fields['presentation'])
    
    s += f"""{badge}<a href="{entry.fields['url']}" target="_blank" class="article-title" style="font-size: 1.1em;">{entry.fields['title']}</a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    
    # Apply both conference name highlighting and oral highlighting
    booktitle_styled = f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>"""
    booktitle_with_conferences = highlight_conference_names(booktitle_styled)
    booktitle_with_oral = highlight_oral_text(booktitle_with_conferences)
    s += f"""{booktitle_with_oral}, {entry.fields['year']} <br>"""

    artefacts = {
        "url": "Paper",
        "code": "Code",
        "html": "Project Page",
        "pdf": "Pdf",
        "supp": "Supplemental",
        "video": "Video",
        "poster": "Poster",
    }
    i = 0
    for k, v in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += " / "
            s += f"""<a href="{entry.fields[k]}" target="_blank" class="article-link">{v}</a>"""
            i += 1
        else:
            print(f"[{entry_key}] Warning: Field {k} missing!")

    # cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    # cite += (
    #     "\tauthor = {"
    #     + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}"
    #     + "}, \n"
    # )
    # for entr in ["title", "booktitle", "year"]:
    #     cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    # cite += """}</pre></code>"""
    # cite = cite.replace("*", "")

    # s += (
    #     " /"
    #     + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    # )
    s += """ </div> </div> </div>"""
    # remove * from cite
    return s


def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    
    # Apply both conference name highlighting and oral highlighting
    booktitle_styled = f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>"""
    booktitle_with_conferences = highlight_conference_names(booktitle_styled)
    booktitle_with_oral = highlight_oral_text(booktitle_with_conferences)
    s += f"""{booktitle_with_oral}, {entry.fields['year']} <br>"""

    artefacts = {"slides": "Slides", "video": "Recording"}
    i = 0
    for k, v in artefacts.items():
        if k in entry.fields.keys():
            if i > 0:
                s += " / "
            s += f"""<a href="{entry.fields[k]}" target="_blank">{v}</a>"""
            i += 1
        else:
            print(f"[{entry_key}] Warning: Field {k} missing!")
    s += """ </div> </div> </div>"""
    return s


def get_publications_html():
    parser = bibtex.Parser()
    bib_data = parser.parse_file("publication_list.bib")
    keys = bib_data.entries.keys()
    s = ""
    for k in keys:
        s += get_paper_entry(k, bib_data.entries[k])
    return s


# def get_talks_html():
#     parser = bibtex.Parser()
#     bib_data = parser.parse_file('talk_list.bib')
#     keys = bib_data.entries.keys()
#     s = ""
#     for k in keys:
#         s+= get_talk_entry(k, bib_data.entries[k])
#     return s


def get_news_items(filename="news.json"):
    with open(filename, "r", encoding="utf-8") as f:
        news_items = json.load(f)
    for item in news_items:
        item["date_obj"] = datetime.strptime(item["date"], "%Y-%m-%d")
    news_items.sort(key=lambda x: x["date_obj"], reverse=True)
    return news_items


def get_news_html():
    news_items = get_news_items()
    s = '<div style="max-height: 250px; overflow-y: auto; padding-right: 10px;"><ul class="list-unstyled" style="font-size: 1.1em;">'
    for item in news_items:
        date_str = item["date_obj"].strftime("%B %d, %Y")
        text_with_conferences = highlight_conference_names(item["text"])  # Apply conference highlighting
        text = highlight_oral_text(text_with_conferences)  # Apply oral highlighting
        s += f"<li style='margin-top: 1em;'><strong>{date_str}</strong>: {text}</li>"
    s += "</ul></div>"
    return s


def get_index_html():
    pub = get_publications_html()
    news_html = get_news_html()
    name, icons_html, bio_text, footer, full_name_en, full_name_ru = get_personal_data()
    ack = get_acknowledgements()
    
    # SEO-optimized title and meta description
    
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  
  <!-- SEO Meta Tags -->
  <title>{full_name_en} - PhD Student in AI Safety & Machine Learning Security</title>
  <meta name="description" content="{full_name_en} ({full_name_ru}) - PhD student at ELLIS/IMPRS-IS Tübingen working on adversarial robustness, AI safety, ML security, and LLM jailbreaking attacks.">
  <meta name="keywords" content="{full_name_en}, {full_name_ru}, Alexander Panfilov, Александр Панфилов, PhD, AI Safety, Machine Learning Security, Adversarial Robustness, LLM Jailbreaking, ELLIS, IMPRS-IS, Tübingen, Jonas Geiping, Maksym Andriushchenko, Max Planck Institute for Intelligent Systems, MPI-IS, Тольятти, Togliatti, Samara, Самара, ITMO, ИТМО, ITMO University, Red Teaming, AI Alignment, ML Security Research">
  <meta name="author" content="{full_name_en}">
  <meta name="robots" content="index, follow">
  
  <!-- Open Graph / Social Media -->
  <meta property="og:type" content="website">
  <meta property="og:title" content="{full_name_en} - AI Safety & ML Security Researcher">
  <meta property="og:description" content="PhD student working on adversarial robustness, AI safety, and LLM jailbreaking attacks at ELLIS Institute Tübingen.">
  <meta property="og:url" content="https://kotekjedi.github.io">
  <meta property="og:image" content="https://kotekjedi.github.io/assets/img/profile_mine_new.jpg">
  
  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{full_name_en} - AI Safety Researcher">
  <meta name="twitter:description" content="PhD student working on adversarial robustness, AI safety, and LLM jailbreaking attacks.">
  <meta name="twitter:image" content="https://kotekjedi.github.io/assets/img/profile_mine_new.jpg">
  <meta name="twitter:site" content="@kotekjedi_ml">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <link rel="icon" type="image/x-icon" href="assets/favicon_mine.ico">
  
  <!-- Structured Data (JSON-LD) for SEO -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "{full_name_en}",
    "alternateName": ["{full_name_ru}", "Sasha Panfilov", "Alexander Panfilov"],
    "jobTitle": "PhD Student",
    "affiliation": {{
      "@type": "Organization",
      "name": "ELLIS Institute Tübingen",
      "alternateName": ["Max Planck Institute for Intelligent Systems", "MPI-IS"]
    }},
    "description": "PhD student working on adversarial robustness, AI safety, ML security, and LLM jailbreaking attacks",
    "url": "https://kotekjedi.github.io",
    "image": "https://kotekjedi.github.io/assets/img/profile_mine_new.jpg",
    "sameAs": [
      "https://scholar.google.com/citations?user=M65_TPEAAAAJ&hl=en",
      "https://www.linkedin.com/in/kotekjedi",
      "https://x.com/kotekjedi_ml",
      "https://github.com/kotekjedi"
    ],
    "knowsAbout": [
      "Artificial Intelligence Safety",
      "Machine Learning Security", 
      "Adversarial Robustness",
      "LLM Jailbreaking",
      "Red Teaming",
      "AI Alignment"
    ],
    "alumniOf": ["ELLIS Institute Tübingen", "ITMO University", "ИТМО"]
  }}
  </script>
  
  <style>
          .article-title {{
              color: #256EFF;
              font-weight: 600;
          }}
          .article-link {{
              color: #256EFF;
          }}
        .profile-pic {{
          width: 90%;
          max-width: 300px;
          height: auto;
          object-fit: cover;
          float: right;
          margin-left: 5%;
          margin-bottom: 15px;
          margin-right: -5%;
          border: 1px solid #ccc;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      }}

      @media (max-width: 767.98px) {{
          .profile-pic {{
              float: none;
              margin-left: auto;
              margin-right: auto;
              margin-bottom: 15px;
              display: block;
          }}
      }}

        .main-container {{
              max-width: 1050px; /* Установите желаемую максимальную ширину */
              margin: 0 auto; /* Центрирует контейнер */
              padding: 0 15px; /* Добавляет отступы по бокам */
          

      }}
    </style>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<!-- Popper.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
<!-- Bootstrap JS -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

<script data-goatcounter="https://kotekjedi.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>
</head>


<body>
    <div class="main-container">

    <div class="container">
        <!-- Заголовок -->
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 0em;">
                <h1 class="display-4 text-center"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h1>
            </div>
        </div>
        <!-- Иконки -->
        <div class="row">
            <div class="col-sm-12">
                {icons_html}
            </div>
        </div>
        <!-- Био и фото -->
        <div class="row" style="margin-top: 2em;">
            <div class="col-md-12">
                {bio_text}
            </div>
        </div>
        <!-- Разделы News и Publications -->
        <div class="row" style="margin-top: 2em;">
            <div class="col-sm-12">
                <h3 style="margin-bottom: 1em; font-weight: bold;">News</h3>
                {news_html}
            </div>
        </div>
        <div class="row" style="margin-top: 2em;">
            <div class="col-sm-12">
                <h3 style="margin-bottom: 1em; font-weight: bold;">Selected Publications</h3>
                {pub}
            </div>
        </div>
        {ack}
    </div>
    {footer}

    </div>

    <!-- Скрипты -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
      integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
      crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"
      integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q"
      crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
      integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl"
      crossorigin="anonymous"></script>
</body>

</html>
    """
    return s


def write_index_html(filename="index.html"):
    s = get_index_html()
    with open(filename, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"Written index content to {filename}.")


if __name__ == "__main__":
    write_index_html("index.html")
