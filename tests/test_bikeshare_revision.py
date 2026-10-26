"""Checks the historical reconciliation and the imported report against their sources."""
import gzip
import base64
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / 'posts/bike-share-navigate'
UPDATED = POST / 'updated-2026-10-13'


class Report(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.in_main = self.in_code = self.in_cell = False
        self.code = []
        self.numbers = []
        self.images = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'main':
            self.in_main = True
        if not self.in_main:
            return
        if tag == 'pre':
            self.in_code = True
            self.code.append('')
        if tag in ('td', 'th'):
            self.in_cell = True
            self.cell = ''
        if tag == 'img':
            self.images.append(attrs['src'])

    def handle_data(self, data):
        if self.in_code:
            self.code[-1] += data
        if self.in_cell:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == 'main':
            self.in_main = False
        if tag == 'pre':
            self.in_code = False
        if tag in ('td', 'th') and self.in_cell:
            self.in_cell = False
            if re.fullmatch(r'-?\d+(?:\.\d+)?', self.cell.strip()):
                self.numbers.append(self.cell.strip())


def check_import():
    provenance = json.loads((UPDATED / 'provenance.json').read_text())
    original = gzip.decompress((UPDATED / 'source-report.html.gz').read_bytes())
    assert hashlib.sha256(original).hexdigest() == provenance['source']['rendered_sha256']
    qmd = gzip.decompress((UPDATED / 'source-report.qmd.gz').read_bytes())
    assert hashlib.sha256(qmd).hexdigest() == provenance['source']['qmd_sha256']
    assert provenance['analysis_reexecuted'] is False
    source = Report(original.decode())
    assert len(source.images) == len(provenance['figures']) == 9
    assert len(source.code) == 14
    for image, figure in zip(source.images, provenance['figures']):
        data = (UPDATED / figure['file']).read_bytes()
        assert data == base64.b64decode(image.split(',', 1)[1], validate=True)
        assert hashlib.sha256(data).hexdigest() == figure['sha256']
    for historical in provenance['historical_articles']:
        data = gzip.decompress((ROOT / historical['path']).read_bytes())
        assert hashlib.sha256(data).hexdigest() == historical['sha256']
    for name in ['pt.qmd', 'index.qmd']:
        article = (POST / name).read_text()
        assert 'date: "2026-10-13"' in article and 'engine: markdown' in article
        assert not re.search(r'^```\{r', article, re.M)
        assert 'file:///' not in article and 'data:image' not in article
        assert len(re.findall(r'^## [1-6]\. ', article, re.M)) == 6
        assert [code.strip() for code in re.findall(r'``` r\n(.*?)\n```', article, re.S)] == [code.strip() for code in source.code]
        tables = re.findall(r'^\|.*(?:\n\|.*)*', article, re.M)[1:]
        assert len(tables) == 5
        numbers = [cell.strip() for table in tables for row in table.splitlines() if row.startswith('|') for cell in row.split('|')[1:-1] if re.fullmatch(r'-?\d+(?:\.\d+)?', cell.strip())]
        assert numbers == source.numbers, name
        images = re.findall(r'!\[([^\]]+)\]\((updated-2026-10-13/[^)]+)\)', article)
        assert len(images) == 9
        assert [Path(target).name for _, target in images] == [figure['file'] for figure in provenance['figures']]
        for target in re.findall(r'\]\(([^)]+)\)', article):
            if not target.startswith(('https://', 'http://', '#')):
                assert (POST / target).is_file(), target
    print('Updated Bike-share: source hashes, 9 unchanged figures, all table values, 14 original code blocks, six phases and PT/EN resources passed.')


def check():
    r = json.loads((POST / 'revision-2026-10-26/results.json').read_text())
    source = r['source']
    assert hashlib.sha256((ROOT / source['frozen']).read_bytes()).hexdigest() == source['frozen_sha256']
    assert hashlib.sha256((ROOT / source['audit_json']).read_bytes()).hexdigest() == source['audit_sha256']
    assert hashlib.sha256((ROOT / r['script']['path']).read_bytes()).hexdigest() == r['script']['sha256']
    assert sum(x['trips'] for x in r['monthly']) == r['retained_trip_rows'] == 4335006
    assert sum(x['trips'] for x in r['calendar_quarters']) == r['retained_trip_rows']
    assert max(r['monthly'], key=lambda x: x['trips'])['month'] == '2021-06'
    assert round(r['duration'][1]['mean_minutes'] / r['duration'][0]['mean_minutes'], 2) == 2.68
    assert round(r['duration'][1]['median_minutes'] / r['duration'][0]['median_minutes'], 2) == 1.77
    for figure in r['figures']:
        assert hashlib.sha256((POST / 'revision-2026-10-26' / figure['file']).read_bytes()).hexdigest() == figure['sha256']
    for name, lang, ratio in [('index.qmd', 'en', '**2.68**'), ('pt.qmd', 'pt', '**2,68**')]:
        article = gzip.decompress((ROOT / 'docs/revisions/2026-10-26-bike-share-replacement' / (name + '.gz')).read_bytes()).decode()
        assert 'engine: markdown' in article and 'date-modified: "2026-10-26"' in article
        assert not re.search(r'^```\{r', article, re.M)
        assert ratio in article and '2021-Q2' in article and '2020-Q3' in article
        assert 'index_files/figure-html' not in article
        for stem in ['monthly-trips', 'bike-types', 'duration-summary']:
            assert f'{stem}-{lang}.png' in article
        for target in re.findall(r'\]\(([^)]+)\)', article):
            if not target.startswith(('https://', 'http://', '#')):
                assert (POST / target).is_file(), target
    before = ROOT / 'docs/revisions/2026-10-26'
    manifest = json.loads((before / 'before-manifest.json').read_text())
    for item in manifest['files']:
        if 'bike-share-navigate' in item['source']:
            restored = gzip.decompress((before / item['archive']).read_bytes())
            assert hashlib.sha256(restored).hexdigest() == item['sha256']
    print('Bike-share reconciliation: counts, duration ratios, hashes, PT/EN figures, static engines and historical snapshots passed.')


if __name__ == '__main__':
    check()
    check_import()
