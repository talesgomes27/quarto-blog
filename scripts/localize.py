"""Localize Quarto navigation after rendering, with usable links without JavaScript."""

import html
import hashlib
import os
import posixpath
import re
import shutil
from pathlib import Path


STYLE_VERSION = hashlib.sha256((Path(__file__).resolve().parents[1] / "styles.css").read_bytes()).hexdigest()[:12]
SITE_URL = "https://talesgomes27.github.io/quarto-blog"
PAIRS = (
    ("index.html", "en/index.html"),
    ("textos.html", "en/textos.html"),
    ("about.html", "en/about.html"),
    ("404.html", "en/404.html"),
    ("posts/bike-share-navigate/pt.html", "posts/bike-share-navigate/index.html"),
    ("posts/bellabeat/index.html", "posts/bellabeat/en.html"),
)
PAGES = {path: (pair, index) for pair in PAIRS for index, path in enumerate(pair)}
HEADER = re.compile(r'<header\b[^>]*\bid=["\']quarto-header["\'][^>]*>.*?</header>', re.S)
ANCHOR = re.compile(r"(<a\b[^>]*>)(.*?)</a>", re.S)
MENU_TEXT = re.compile(r'(<span\b[^>]*\bclass=["\']menu-text["\'][^>]*>)(.*?)(</span>)', re.S)
ALTERNATES = re.compile(r"\n?<!-- language-alternates -->.*?<!-- /language-alternates -->\n?", re.S)


def attribute(tag, name):
    match = re.search(rf'\s{re.escape(name)}\s*=\s*(["\'])(.*?)\1', tag, re.S)
    return html.unescape(match[2]) if match else ""


def set_attribute(tag, name, value):
    pattern = rf'\s{re.escape(name)}\s*=\s*(["\'])(.*?)\1'
    tag = re.sub(pattern, "", tag, flags=re.S)
    if value is not None:
        tag = tag[:-1] + f' {name}="{html.escape(value, quote=True)}">'
    return tag


def relative(target, page):
    path, separator, fragment = target.partition("#")
    return posixpath.relpath(path, posixpath.dirname(page) or ".") + (separator + fragment)


def localize(document, page):
    if "netflix-amazon-comparison" in page.split("/"):
        return document
    pair, language = PAGES.get(page, (("index.html", "en/index.html"), 0))
    english = language == 1
    home = "en/index.html" if english else "index.html"
    writing = "en/textos.html" if english else "textos.html"
    about = "en/about.html" if english else "about.html"
    menus = {
        "Projetos": ("Projects" if english else "Projetos", home + "#projetos"),
        "Projects": ("Projects" if english else "Projetos", home + "#projetos"),
        "Textos": ("Writing" if english else "Textos", writing),
        "Writing": ("Writing" if english else "Textos", writing),
        "Sobre": ("About" if english else "Sobre", about),
        "About": ("About" if english else "Sobre", about),
        "Contato": ("Contact" if english else "Contato", "mailto:talesgomes27@gmail.com"),
        "Contact": ("Contact" if english else "Contato", "mailto:talesgomes27@gmail.com"),
    }

    def anchor(match):
        tag, body = match.groups()
        if "quarto-color-scheme-toggle" in attribute(tag, "class").split():
            name = "Switch between light and dark themes" if english else "Alternar entre tema claro e escuro"
            return set_attribute(set_attribute(tag, "aria-label", name), "title", name) + body + "</a>"
        if "navbar-brand" in attribute(tag, "class").split():
            return set_attribute(tag, "href", relative(home, page)) + body + "</a>"
        span = MENU_TEXT.search(body)
        label = html.unescape(re.sub(r"<[^>]+>", "", span[2])).strip() if span else ""
        if label not in menus and label not in ("PT", "EN"):
            return match[0]
        classes = [value for value in attribute(tag, "class").split() if value != "active"]
        tag = set_attribute(tag, "aria-current", None)
        if label in ("PT", "EN"):
            active = (label == "EN") == english
            tag = set_attribute(tag, "href", relative(pair[label == "EN"], page))
            tag = set_attribute(tag, "hreflang", "en" if label == "EN" else "pt-BR")
            tag = set_attribute(tag, "lang", "en" if label == "EN" else "pt-BR")
        else:
            translated, target = menus[label]
            active = target.partition("#")[0] == page
            tag = set_attribute(tag, "href", target if target.startswith("mailto:") else relative(target, page))
            body = MENU_TEXT.sub(lambda part: part[1] + translated + part[3], body, count=1)
        if active:
            classes.append("active")
            tag = set_attribute(tag, "aria-current", "true" if label in ("PT", "EN") else "page")
        tag = set_attribute(tag, "class", " ".join(classes))
        return tag + body + "</a>"

    # A new theme must not be combined with an older cached custom stylesheet.
    def stylesheet(match):
        tag = match[0]
        path = attribute(tag, "href").partition("?")[0]
        if path.rsplit("/", 1)[-1] == "styles.css":
            return set_attribute(tag, "href", f"{path}?v={STYLE_VERSION}")
        return tag

    document = re.sub(r"<link\b[^>]*>", stylesheet, document)
    document = HEADER.sub(lambda match: ANCHOR.sub(anchor, match[0]), document, count=1)
    document = re.sub(r"<html\b[^>]*>", lambda match: set_attribute(match[0], "lang", "en" if english else "pt-BR"), document, count=1)
    document = re.sub(
        r'(<span\b[^>]*\bid=["\']footer-copy["\'][^>]*>).*?(</span>)',
        lambda match: match[1] + ("Made with Quarto. By Tales Gomes." if english else "Feito com Quarto. Por Tales Gomes.") + match[2],
        document, count=1, flags=re.S,
    )
    if page in ("textos.html", "en/textos.html"):
        document = re.sub(
            r'(src=["\'][^"\']*/quarto-listing\.js)(?:\?[^"\']*)?(["\'])',
            r'\1?v=1.10.19\2', document,
        )
        document = re.sub(
            r'<input\b[^>]*class=["\']search form-control["\'][^>]*>',
            lambda match: set_attribute(match[0], "aria-label", "Filter studies" if english else "Filtrar estudos"),
            document,
        )
        # Native buttons preserve Quarto's click handlers and also work with Enter/Space.
        document = re.sub(
            r'<div(\s[^>]*\bclass=["\'](?:category|listing-category)["\'][^>]*)>(.*?)</div>',
            lambda match: '<button type="button"' + match[1] + '>' + match[2] + '</button>',
            document, flags=re.S,
        )
    document = ALTERNATES.sub("", document)
    if page in PAGES:
        alternatives = "\n<!-- language-alternates -->\n" + "\n".join(
            f'<link rel="alternate" hreflang="{lang}" href="{SITE_URL}/{target}">'
            for lang, target in (("pt-BR", pair[0]), ("en", pair[1]), ("x-default", pair[0]))
        ) + "\n<!-- /language-alternates -->\n"
        document = document.replace("</head>", alternatives + "</head>", 1)
    return document


def main():
    root = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
    # Historical freeze assets otherwise overwrite the renderer's current category decoder.
    listing_runtime = root / "site_libs/quarto-listing/quarto-listing.js"
    if listing_runtime.is_file():
        shutil.copyfile(Path(__file__).parent / "vendor/quarto-listing.js", listing_runtime)
    for path in root.rglob("*.html"):
        page = path.relative_to(root).as_posix()
        if "site_libs" in path.relative_to(root).parts or "netflix-amazon-comparison" in path.relative_to(root).parts:
            continue
        original = path.read_text(encoding="utf-8")
        updated = localize(original, page)
        if updated != original:
            path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
