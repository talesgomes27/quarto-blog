"""Checks the published reconciliation against its pinned archived evidence."""
import gzip
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / 'posts/bike-share-navigate'


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
        article = (POST / name).read_text()
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
