"""Check static project imports, source preservation and bilingual reading features."""

import gzip
import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('localize', ROOT / 'scripts/localize.py')
localize = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(localize)
PROJECTS = {'ecommerce': (9, 10), 'sherlock': (3, 5), 'fraud': (8, 2), 'youtube': (5, 8)}


class Report(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.pre = False
        self.cell = False
        self.codes = []
        self.tables = []
        self.links = []
        self.images = []
        self.annotation = False
        self.math = False
        self.main = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main':
            self.main = True
        if not self.main:
            return
        if tag == 'math':
            self.math = True
        elif tag == 'annotation':
            self.annotation = True
        elif tag == 'pre':
            self.pre = True
            self.codes.append('')
        elif tag == 'table':
            self.tables.append([])
        elif tag in ('td', 'th'):
            self.cell = True
            self.tables[-1].append('')
        elif tag == 'a':
            self.links.append(attrs)
        elif tag == 'img':
            self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'main':
            self.main = False
        elif tag == 'math':
            self.math = False
        elif tag == 'annotation':
            self.annotation = False
        elif tag == 'pre':
            self.pre = False
        elif tag in ('td', 'th'):
            self.cell = False

    def handle_data(self, data):
        if not self.main or (self.math and not self.annotation):
            return
        if self.pre:
            self.codes[-1] += data
        if self.cell:
            self.tables[-1][-1] += data


def numbers(table):
    # Ignore translated labels and TeX's decimal-brace notation, retaining values.
    text = ' '.join(table).replace('{,}', ',').replace('{.}', '.')
    return re.findall(r'\d+(?:[.,]\d+)*', text)


def check():
    for slug, (figure_count, table_count) in PROJECTS.items():
        post = ROOT / 'posts' / slug
        pair = (f'posts/{slug}/index.html', f'posts/{slug}/en.html')
        assert pair in localize.PAIRS, f'Missing translation pair: {slug}'
        provenance = json.loads((post / 'provenance.json').read_text())
        assert provenance['analysis_reexecuted'] is False
        assert re.fullmatch('[0-9a-f]{40}', provenance['source_blob_sha'])
        for snapshot in provenance['snapshots']:
            data = gzip.decompress((post / snapshot['file']).read_bytes())
            assert hashlib.sha256(data).hexdigest() == snapshot['uncompressed_sha256']
            if snapshot['file'].endswith('.qmd.gz'):
                blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                assert blob == provenance['source_blob_sha'], (slug, 'source differs from GitHub blob')
        assert len(provenance['figures']) == figure_count
        for figure in provenance['figures']:
            source = (post / figure['file']).read_bytes()
            assert hashlib.sha256(source).hexdigest() == figure['sha256']
            assert (ROOT / '_site/posts' / slug / figure['file']).read_bytes() == source
        original = Report(gzip.decompress((post / 'source/report.html.gz').read_bytes()).decode())
        assert len(original.tables) == table_count, slug
        for filename, language in [('index', 'pt-BR'), ('en', 'en')]:
            source = (post / f'{filename}.qmd').read_text()
            assert 'engine: markdown' in source and 'freeze: false' in source
            assert not re.search(r'^```\{(?:python|r|julia)', source, re.M)
            assert re.search(r'^author: ["\']?Tales Gomes["\']?$', source, re.M)
            assert f'date: "{provenance["report_date"]}"' in source
            assert '{{< cite-this page collapsed=true >}}' in source
            for resource in ('provenance.json', 'source/report.html.gz', 'source/report.qmd.gz'):
                assert resource in source
                assert (ROOT / '_site/posts' / slug / resource).is_file()
            output = (ROOT / '_site/posts' / slug / f'{filename}.html').read_text()
            rendered = Report(output)
            assert f'lang="{language}"' in output
            assert 'lightbox' in output and 'glightbox' in output.lower()
            assert len([img for img in rendered.images if img.get('src', '').startswith('figures/')]) == figure_count
            assert [numbers(table) for table in rendered.tables] == [numbers(table) for table in original.tables], (slug, filename, 'table numbers changed')
            assert [code.strip() for code in rendered.codes[:len(original.codes)]] == [code.strip() for code in original.codes], (slug, filename, 'displayed code changed')
            for link in rendered.links:
                target = link.get('href', '')
                if target.startswith('#') and len(target) > 1:
                    assert f'id="{target[1:]}"' in output, (slug, filename, target)
    print('Project posts: immutable sources/figures, original numeric tables/code, PT/EN routes, lightbox and static engines passed.')


if __name__ == '__main__':
    check()
