"""Run directly; optionally pass the completed site directory to verify its pairs."""

import importlib.util
import os
import posixpath
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("localize", Path(__file__).parents[1] / "scripts/localize.py")
localize = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(localize)


class Links(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.links = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        if tag in ("a", "link"):
            self.links.append(dict(attrs))


def fixture():
    # Quarto's navbar structure, including its native search and Bootstrap control.
    header = '''<html lang="pt-BR"><head><title>Portal</title></head><body>
<header id="quarto-header" class="headroom fixed-top"><nav class="navbar">
<a class="navbar-brand" href="./index.html"><span class="navbar-title">Tales Gomes</span></a>
<div id="quarto-search" title="Pesquisar"></div>
<button class="navbar-toggler" data-bs-target="#navbarCollapse" aria-expanded="false">Menu</button>
<div id="navbarCollapse"><ul>'''
    for label in ("Projetos", "Textos", "Sobre", "Contato", "PT", "EN"):
        header += f'<li class="nav-item"><a class="nav-link active" href="./index.html" aria-current="page"><span class="menu-text">{label}</span></a></li>'
    return header + '''</ul></div><a class="quarto-color-scheme-toggle" href="" onclick="window.quartoToggleColorScheme(); return false;" title="Alternar modo escuro"><i class="bi"></i></a></nav></header>
<main><a href="keep.html">Conteúdo intacto</a><script>const untouched = true;</script></main>
<footer><span id="footer-copy">Feito com Quarto. Por Tales Gomes.</span></footer>
<script src="site_libs/quarto-nav/quarto-nav.js"></script></body></html>'''


def test_localization():
    source = fixture()
    for pair in localize.PAIRS:
        for index, page in enumerate(pair):
            result = localize.localize(source, page)
            assert localize.localize(result, page) == result, page
            assert f'<html lang="{"en" if index else "pt-BR"}">' in result
            links = Links(result).links
            language_links = [link for link in links if link.get("hreflang") in ("en", "pt-BR") and "class" in link]
            assert len(language_links) == 2
            for language_link in language_links:
                target = posixpath.normpath(posixpath.join(posixpath.dirname(page), language_link["href"]))
                assert target == pair[language_link["hreflang"] == "en"]
                active = language_link["hreflang"] == ("en" if index else "pt-BR")
                assert (language_link.get("aria-current") == "true") == active
                assert ("active" in language_link["class"].split()) == active
            assert '<div id="quarto-search" title="Pesquisar"></div>' in result
            assert '<button class="navbar-toggler" data-bs-target="#navbarCollapse" aria-expanded="false">Menu</button>' in result
            assert '<main><a href="keep.html">Conteúdo intacto</a><script>const untouched = true;</script></main>' in result
            assert '<script src="site_libs/quarto-nav/quarto-nav.js"></script>' in result
            toggle_name = "Switch between light and dark themes" if index else "Alternar entre tema claro e escuro"
            assert f'aria-label="{toggle_name}"' in result
            assert 'onclick="window.quartoToggleColorScheme(); return false;"' in result
            assert result.count('rel="alternate"') == 3
            for language, target in (("pt-BR", pair[0]), ("en", pair[1]), ("x-default", pair[0])):
                assert f'hreflang="{language}" href="{localize.SITE_URL}/{target}"' in result
            for label in (("Projects", "Writing", "About", "Contact") if index else ("Projetos", "Textos", "Sobre", "Contato")):
                assert f'>{label}</span>' in result
            assert ("Made with Quarto. By Tales Gomes." in result) == bool(index)
    styled = source.replace("</head>", '<link rel="stylesheet" href="../styles.css?old=1"></head>')
    styled_result = localize.localize(styled, "en/index.html")
    assert f'href="../styles.css?v={localize.STYLE_VERSION}"' in styled_result
    assert localize.localize(styled_result, "en/index.html") == styled_result
    assert localize.localize(source, "posts/netflix-amazon-comparison/index.html") == source
    fallback = localize.localize(source, "other/page.html")
    assert 'hreflang="en"' in fallback and 'href="../en/index.html"' in fallback
    assert 'rel="alternate"' not in fallback


def test_archive_controls():
    source = fixture().replace("</main>", """<input class="search form-control" placeholder="Filtro">
<div class="category" data-category="Ug==">R <span>(2)</span></div>
<div class="listing-category" onclick="keepHandler()">R</div></main>""")
    for page, label in [("textos.html", "Filtrar estudos"), ("en/textos.html", "Filter studies")]:
        result = localize.localize(source, page)
        assert f'aria-label="{label}"' in result
        assert '<button type="button" class="category" data-category="Ug==">R <span>(2)</span></button>' in result
        assert '<button type="button" class="listing-category" onclick="keepHandler()">R</button>' in result
        assert localize.localize(result, page) == result
    assert '<div class="category"' in localize.localize(source, "about.html")


def test_render_hook():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for page in ("index.html", "en/index.html", "site_libs/library.html", "posts/netflix-amazon-comparison/index.html"):
            path = root / page
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(fixture())
        runtime = root / "site_libs/quarto-listing/quarto-listing.js"
        runtime.parent.mkdir(parents=True, exist_ok=True)
        runtime.write_text("historical runtime")
        previous = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR")
        os.environ["QUARTO_PROJECT_OUTPUT_DIR"] = directory
        try:
            localize.main()
            assert runtime.read_bytes() == (Path(localize.__file__).parent / "vendor/quarto-listing.js").read_bytes()
            assert ">Projects</span>" in (root / "en/index.html").read_text()
            for page in ("site_libs/library.html", "posts/netflix-amazon-comparison/index.html"):
                assert (root / page).read_text() == fixture()
            first = (root / "en/index.html").read_text()
            localize.main()
            assert (root / "en/index.html").read_text() == first
        finally:
            if previous is None:
                os.environ.pop("QUARTO_PROJECT_OUTPUT_DIR", None)
            else:
                os.environ["QUARTO_PROJECT_OUTPUT_DIR"] = previous


def validate_site(root):
    for pair in localize.PAIRS:
        for page in pair:
            path = root / page
            assert path.is_file(), f"Missing translated page: {path}"
            result = path.read_text()
            assert localize.localize(result, page) == result, f"Post-render localization missing: {page}"
            for link in Links(result).links:
                if link.get("hreflang") in ("pt-BR", "en") and "class" in link:
                    assert (path.parent / link["href"]).is_file(), f"Broken language link: {page}: {link['href']}"


    for page in localize.PAGES:
        document = (root / page).read_text()
        assert 'class="quarto-color-scheme-toggle' in document, page
        assert 'data-mode="dark"' in document and 'data-mode="light"' in document, page
        assert f'styles.css?v={localize.STYLE_VERSION}' in document, page
    assert (root / "site_libs/quarto-listing/quarto-listing.js").read_bytes() == (Path(localize.__file__).parent / "vendor/quarto-listing.js").read_bytes()
    for pair in localize.PAIRS[-2:]:
        for page, locale in zip(pair, ("pt", "en")):
            document = (root / page).read_text()
            assert 'script.src = "https://giscus.app/client.js";' in document, page
            assert f'script.dataset.lang = "{locale}";' in document, page
            assert 'script.dataset.repoId = "R_kgDOHeSMkg";' in document, page
            assert 'script.dataset.categoryId = "DIC_kwDOHeSMks4CPoEN";' in document, page
            assert 'script.dataset.mapping = "title";' in document, page
            assert 'id="giscus-alt-theme" value="dark_dimmed"' in document, page


if __name__ == "__main__":
    test_localization()
    test_archive_controls()
    test_render_hook()
    if len(sys.argv) > 1:
        validate_site(Path(sys.argv[1]))
    print("Language navigation checks passed.")
