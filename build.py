import json
import time
from datetime import datetime

from pybtex.database.input import bibtex


def get_personal_data():
    name = ["Alexander", "Panfilov"]
    email = "micniemeyer1@gmail.com"
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
        <img src="assets/img/profile_mine.jpg" alt="Profile picture" class="profile-pic" style="float: right; margin-left: 35px; margin-bottom: 15px; margin-right: -85px;">

        <p style="font-size: 1.2em;">
            Yo! My name is <span style="font-weight: 500;">Sasha</span>
  and I am a first-year ELLIS / IMPRS-IS PhD student, based in Tübingen. I am very lucky to be working under the supervision of<a href="https://jonasgeiping.github.io/" class="m-2" style="font-weight: 500;">Jonas Geiping</a>and<a href="https://www.andriushchenko.me/" class="m-2" style="font-weight: 500;">Maksym Andriushchenko</a>.
        </p>
        <p style="font-size: 1.2em;">
        Broadly, I am interested in adversarial robustness, AI safety, and ML security. In practical terms, I like to break machine learning systems in various ways. Lately, I’ve been focusing on jailbreaking attacks on LLMs and what they mean for safety and security.
        </p>
        <p style="font-size: 1.2em;">
        You can find my CV <a href="{cv}" target="_blank" style="text-decoration: none; color: inherit; background-color: rgb(255, 255, 179);">here</a>. I am always open to collaboration — feel free to reach out via email!</p>
    """
    current_date = time.strftime("%d/%m/%Y")
    footer = f"""
    <footer style="text-align: right; padding: 10px; margin-top: 20px;">
        <p style="font-size: 0.9em;">
            Updated on {current_date}. Website design credits to <a href="https://github.com/m-niemeyer/m-niemeyer.github.io" target="_blank">Michael Niemeyer</a>.
        </p>
    </footer>
    """

    return name, icons_html, bio_text, footer


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


def get_paper_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;" > <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid" alt="Project image">"""
    s += """</div><div class="col-sm-9" style="font-size: 1.1em;">"""

    s += f"""<a href="{entry.fields['url']}" target="_blank" class="article-title" style="font-size: 1.15em;">{entry.fields['title']}</a> <br>"""

    s += f"""{generate_person_html(entry.persons['author'])} <br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

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

    cite = "<pre><code>@InProceedings{" + f"{entry_key}, \n"
    cite += (
        "\tauthor = {"
        + f"{generate_person_html(entry.persons['author'], make_bold=False, add_links=False, connection=' and ')}"
        + "}, \n"
    )
    for entr in ["title", "booktitle", "year"]:
        cite += f"\t{entr} = " + "{" + f"{entry.fields[entr]}" + "}, \n"
    cite += """}</pre></code>"""
    cite = cite.replace("*", "")

    s += (
        " /"
        + f"""<button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapse{entry_key}" aria-expanded="false" aria-controls="collapseExample" style="margin-left: -6px; margin-top: -2px;">Expand bibtex</button><div class="collapse" id="collapse{entry_key}"><div class="card card-body">{cite}</div></div>"""
    )
    s += """ </div> </div> </div>"""
    # remove * from cite
    return s


def get_talk_entry(entry_key, entry):
    s = """<div style="margin-bottom: 3em;"> <div class="row"><div class="col-sm-3">"""
    s += f"""<img src="{entry.fields['img']}" class="img-fluid img-thumbnail" alt="Project image">"""
    s += """</div><div class="col-sm-9">"""
    s += f"""{entry.fields['title']}<br>"""
    s += f"""<span style="font-style: italic;">{entry.fields['booktitle']}</span>, {entry.fields['year']} <br>"""

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
    s = '<ul class="list-unstyled" style="font-size: 1.1em;">'
    for item in news_items:
        date_str = item["date_obj"].strftime("%B %d, %Y")
        text = item["text"]
        s += f"<li><strong>{date_str}</strong>: {text}</li>"
    s += "</ul>"
    return s


def get_index_html():
    pub = get_publications_html()
    news_html = get_news_html()
    name, icons_html, bio_text, footer = get_personal_data()
    s = f"""
    <!doctype html>
<html lang="en">

<head>
  <!-- Required meta tags -->
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
    integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

  <title>{name[0] + ' ' + name[1]}</title>
  <link rel="icon" type="image/x-icon" href="assets/favicon_mine.ico">
  <style>
          .article-title {{
              color: #256EFF;
              font-weight: 600;
          }}
          .article-link {{
              color: #256EFF;
          }}
          .profile-pic {{
          width: 251px; /* Установите желаемую ширину */
          height: 251px; /* Высота должна быть равна ширине для круга */
          border-radius: 50%; /* Делает изображение кругом */
          border: 1px solid #ccc;
          box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
          object-fit: cover; /* Обрезает изображение по контейнеру без искажения */
          }}
        .main-container {{
              max-width: 1200px; /* Установите желаемую максимальную ширину */
              margin: 0 auto; /* Центрирует контейнер */
              padding: 0 15px; /* Добавляет отступы по бокам */
          

      }}
    </style>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<!-- Popper.js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"></script>
<!-- Bootstrap JS -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>

</head>


<body>
    <div class="main-container">

    <div class="container">
        <!-- Заголовок -->
        <div class="row" style="margin-top: 3em;">
            <div class="col-sm-12" style="margin-bottom: 0em;">
                <h3 class="display-4 text-center"><span style="font-weight: bold;">{name[0]}</span> {name[1]}</h3>
            </div>
        </div>
        <!-- Иконки -->
        <div class="row">
            <div class="col-sm-12">
                {icons_html}
            </div>
        </div>
        <!-- Био и фото -->
        <div class="row" style="margin-top: 1em;">
            <div class="col-md-10">
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
                <h3 style="margin-bottom: 1em; font-weight: bold;">Publications</h3>
                {pub}
            </div>
        </div>
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
