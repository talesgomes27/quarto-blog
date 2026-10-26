"""Refresh the offline Quarto extension index; never install or execute extensions."""

import hashlib
import json
import os
import tempfile
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / 'docs/quarto-extensions'
SOURCES = {
    'shortcodes-filters': 'https://quarto.org/docs/extensions/',
    'journal-articles': 'https://quarto.org/docs/extensions/listing-journals.html',
    'custom-formats': 'https://quarto.org/docs/extensions/listing-formats.html',
    'revealjs': 'https://quarto.org/docs/extensions/listing-revealjs.html',
}


class Listing(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_listing = False
        self.cells = []
        self.cell = None
        self.repository = None
        self.entries = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table' and 'quarto-listing-table' in attrs.get('class', '').split():
            self.in_listing = True
        if not self.in_listing:
            return
        if tag == 'tr':
            self.cells, self.repository = [], None
        elif tag == 'td':
            self.cell = []
        elif tag == 'a' and 'listing-name' in attrs.get('class', '').split():
            self.repository = attrs.get('href')

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == 'td' and self.cell is not None:
            self.cells.append(' '.join(''.join(self.cell).split()))
            self.cell = None
        elif tag == 'tr' and self.repository:
            if len(self.cells) != 3 or not all(self.cells):
                raise ValueError('Unexpected Quarto listing columns; previous index retained.')
            name, description, author = self.cells
            self.entries.append(dict(name=name, description=description, author=author,
                                     repository=self.repository))
            self.repository = None
        elif tag == 'table':
            self.in_listing = False


def build_catalog(pages, checked_at):
    entries, sources = {}, []
    for category, url in SOURCES.items():
        raw = pages[category]
        parser = Listing()
        parser.feed(raw.decode('utf-8'))
        if not parser.entries:
            raise ValueError(f'Empty listing for {category}; previous index retained.')
        sources.append(dict(category=category, url=url, entries=len(parser.entries),
                            sha256=hashlib.sha256(raw).hexdigest()))
        for entry in parser.entries:
            key = (entry['name'], entry['repository'])
            if key not in entries:
                entries[key] = dict(entry, categories=[])
            if category not in entries[key]['categories']:
                entries[key]['categories'].append(category)
    extensions = sorted(entries.values(), key=lambda item: (item['name'].casefold(), item['repository']))
    return dict(checked_at=checked_at, scope='Four official Quarto extension listings; not the entire ecosystem.',
                validation='Listed functionality only; installation and compatibility require separate review.',
                sources=sources, extension_count=len(extensions), extensions=extensions)


def markdown(catalog):
    def cell(value):
        return value.replace('|', '\\|').replace('\n', ' ')

    lines = ['# Catálogo local de extensões Quarto', '',
             f"Consulta: {catalog['checked_at']}. {catalog['extension_count']} extensões distintas nas quatro listagens oficiais.",
             '', 'Índice de descoberta; presença nesta lista não comprova compatibilidade, segurança ou instalação.',
             'As descrições funcionais mantêm o idioma do catálogo de origem. Veja a curadoria em [README.md](README.md).', '']
    for category, url in SOURCES.items():
        lines += [f'## {category}', '', f'Fonte: [{category}]({url}).', '',
                  '| Extensão | Funcionalidade declarada | Autor |', '| --- | --- | --- |']
        for entry in catalog['extensions']:
            if category in entry['categories']:
                lines.append(f"| [{cell(entry['name'])}]({entry['repository']}) | {cell(entry['description'])} | {cell(entry['author'])} |")
        lines.append('')
    return '\n'.join(lines)


def replace_file(path, content):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                                     delete=False) as handle:
        temporary = Path(handle.name)
        handle.write(content)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    pages = {}
    for category, url in SOURCES.items():
        request = Request(url, headers={'User-Agent': 'quarto-blog-extension-index'})
        with urlopen(request, timeout=30) as response:
            pages[category] = response.read()
    catalog = build_catalog(pages, datetime.now(ZoneInfo('America/Belem')).date().isoformat())
    output = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    readable = markdown(catalog)
    DESTINATION.mkdir(parents=True, exist_ok=True)
    replace_file(DESTINATION / 'catalog.json', output)
    replace_file(DESTINATION / 'catalog.md', readable)
    print(f"Updated {catalog['extension_count']} distinct extensions from four official listings.")


if __name__ == '__main__':
    main()
