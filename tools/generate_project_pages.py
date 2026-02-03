from pathlib import Path
import html
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
cards_path = ROOT / "html" / "cards.html"
out_dir = ROOT / "projects"
out_dir.mkdir(exist_ok=True)

soup = BeautifulSoup(cards_path.read_text(encoding="utf-8"), "html.parser")

def outer_html(tag):
    return str(tag) if tag else ""

def clean_hidden(tag):
    if not tag:
        return ""
    if tag.has_attr("style") and "display:none" in tag["style"].replace(" ", ""):
        del tag["style"]
    for t in tag.find_all(True):
        if t.has_attr("style") and "display:none" in t["style"].replace(" ", ""):
            del t["style"]
    return str(tag)

written = 0
for card in soup.select(".project-card"):
    slug = card.get("data-slug", "").strip()
    if not slug:
        continue

    title_tag = card.find("h3")
    title = title_tag.get_text(strip=True) if title_tag else slug

    skills = card.find("div", class_="skills")
    responsible = card.find("p", class_="responsible")
    target = card.find("p", class_="target")
    duration = card.find("p", class_="duration")
    areas = card.find("p", class_="areas")
    scope = card.find(class_="scope")

    duration_text = duration.get_text(strip=True) if duration else ""

    # show even hidden fields on the static page
    areas_html = clean_hidden(areas)
    scope_html = clean_hidden(scope)

    qmd = f"""---
title: "{html.escape(title)}"
format:
  html:
    theme: cosmo
    css: ../css/style.css
    toc: false
---

<div class="project-detail">
{outer_html(skills)}
<p class="duration"><strong>Duration:</strong> {html.escape(duration_text)}</p>
{outer_html(responsible)}
{outer_html(target)}
{areas_html}
{scope_html}
</div>

<p>
  <a href="../index.html#projects" class="project-link-btn">
    ← Back to all projects
  </a>
</p>
"""
    (out_dir / f"{slug}.qmd").write_text(qmd, encoding="utf-8")
    written += 1

print(f"Wrote {written} project pages into {out_dir}/")
