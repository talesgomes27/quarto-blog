"""Check corrected results against the preserved inputs and independent Python audit."""
import gzip
import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / 'posts/bellabeat'
OUTPUT = POST / 'revision-2026-10-26'


def check():
    baseline = ROOT / 'docs/revisions/2026-10-26'
    manifest = json.loads((baseline / 'before-manifest.json').read_text())
    for item in manifest['files']:
        restored = gzip.decompress((baseline / item['archive']).read_bytes())
        assert hashlib.sha256(restored).hexdigest() == item['sha256'], item['source']
        if item['source'].startswith('_freeze/'):
            assert (ROOT / item['source']).read_bytes() == restored, item['source']

    spec = importlib.util.spec_from_file_location('audit_bellabeat', ROOT / 'scripts/audit_bellabeat.py')
    audit = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(audit)
    old = audit.audit()
    revised = json.loads((OUTPUT / 'results.json').read_text())
    assert revised['rows'] == revised['unique_user_days'] == old['unique_user_days'] == 940
    assert old['rows'] == 943 and revised['removed_exact_sleep_duplicates'] == 3
    assert revised['long_rows'] == revised['rows'] * 4 == 3760
    for field, expected in old['exact_user_day_deduplicated_sensitivity'].items():
        actual = revised['summary'][field]
        for key in ('observations', 'users', 'missing'):
            assert actual[key] == expected[key], (field, key)
        for key in ('mean', 'min', 'max'):
            assert math.isclose(actual[key], expected[key], abs_tol=1e-5, rel_tol=0), (field, key)
    days = ['seg', 'ter', 'qua', 'qui', 'sex', 'sáb', 'dom']
    for actual in revised['weekday']:
        expected = old['weekday_sensitivity'][days[actual['weekday'] - 1]]
        assert actual['observations'] == expected['unique_user_days']
        assert actual['dates'] == expected['dates']
        for field in ('mean_distance_km', 'mean_steps'):
            assert math.isclose(actual[field], expected[field], abs_tol=1e-5, rel_tol=0)
    assert sum(group['observations'] for group in revised['sleep_groups'].values()) == 410
    assert revised['sleep_groups']['6to10']['observations'] == 292

    provenance = json.loads((OUTPUT / 'provenance.json').read_text())
    assert provenance['checks']['unique_keys_verified']
    assert provenance['source']['sha256'] == '4741dfabd18453de19b6dd0a7204e8fea6e45e70bc9ddbe396956c8e4fde02f8'
    assert hashlib.sha256((ROOT / provenance['script']).read_bytes()).hexdigest() == provenance['script_sha256']
    for name, digest in provenance['outputs_sha256'].items():
        assert hashlib.sha256((OUTPUT / name).read_bytes()).hexdigest() == digest, name

    for name, lang in [('index.qmd', 'pt'), ('en.qmd', 'en')]:
        article = (POST / name).read_text()
        assert 'engine: markdown' in article and 'freeze: false' in article
        assert 'date: "2021-09-10"' in article and 'date-modified: "2026-10-26"' in article
        assert not re.search(r'^```\{r', article, re.M)
        assert 'index_files/figure-html' not in article
        for table in ('summary', 'sleep', 'weekday', 'comparison'):
            assert f'{table}-{lang}.md' in article
        for target in re.findall(r'\]\(([^)]+)\)', article):
            if not target.startswith(('https://', 'http://', '#')):
                assert (POST / target).is_file(), target
    print('Study corrections: baseline, frozen inputs, independent summaries, weekday coverage, hashes and PT/EN resources passed.')


if __name__ == '__main__':
    check()
