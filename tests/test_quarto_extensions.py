"""Offline parser checks: nested markup, duplicate categories and failed refreshes."""

import importlib.util
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('extensions', ROOT / 'scripts/update_quarto_extensions.py')
extensions = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extensions)


def check():
    fixture = b'''<table><tr><td>Unrelated navigation</td></tr></table>
<table class="table quarto-listing-table"><tbody><tr>
<td><a class="name listing-name" href="https://github.com/example/filter">filter</a></td>
<td><span>Show <a href="https://example.org">code</a> &amp; figures.</span></td>
<td><a href="https://github.com/example">Example Author</a></td>
</tr></tbody></table>'''
    pages = {category: fixture for category in extensions.SOURCES}
    catalog = extensions.build_catalog(pages, '2026-10-26')
    assert catalog['extension_count'] == 1
    entry = catalog['extensions'][0]
    assert entry['categories'] == list(extensions.SOURCES)
    assert entry['description'] == 'Show code & figures.'
    assert entry['repository'] == 'https://github.com/example/filter'
    assert all(source['entries'] == 1 for source in catalog['sources'])
    assert extensions.markdown(catalog).count('[filter]') == 4
    pages['revealjs'] = b'<html>A temporary upstream error page</html>'
    try:
        extensions.build_catalog(pages, '2026-10-26')
    except ValueError:
        pass
    else:
        raise AssertionError('An empty/error page must not replace the cached catalog.')
    installed = json.loads((ROOT / 'docs/quarto-extensions/installed.json').read_text())
    for extension in [installed] + installed.get('additional_extensions', []):
        for item in extension['files']:
            data = (ROOT / extension['installed_path'] / item['file']).read_bytes()
            assert hashlib.sha256(data).hexdigest() == item['installed_sha256'], item['file']
            if item['file'] not in ('remember.js', 'link-previews.js', 'cite-this.lua'):
                assert item['upstream_sha256'] == item['installed_sha256'], item['file']
    for name in ['bike-share-navigate/pt', 'bike-share-navigate/index', 'bellabeat/index', 'bellabeat/en']:
        article = (ROOT / 'posts' / (name + '.qmd')).read_text()
        assert 'filters:\n  - remember' in article
        assert 'engine: markdown' in article
    print('Extension index: nested markup, deduplication and invalid-source rejection passed.')
    print('Extensions: pinned asset hashes and remember activation in the four static articles passed.')


if __name__ == '__main__':
    check()
