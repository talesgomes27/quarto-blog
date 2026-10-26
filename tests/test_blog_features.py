"""Validate rendered previews, citations, sharing links and bilingual RSS offline."""

import importlib.util
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('localize', ROOT / 'scripts/localize.py')
localize = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(localize)


class Links(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'link'):
            self.links.append(dict(attrs))


def check():
    for prefix, language, expected in [('', 'pt-BR', ['posts/bike-share-navigate/pt.html', 'posts/bellabeat/index.html']),
                                       ('en/', 'en', ['posts/bike-share-navigate/index.html', 'posts/bellabeat/en.html'])]:
        feed = ET.parse(ROOT / '_site' / (prefix + 'textos.xml')).getroot().find('channel')
        assert feed.findtext('language') == language
        assert [item.findtext('link') for item in feed.findall('item')] == [localize.SITE_URL + '/' + path.removesuffix('index.html') for path in expected]
        assert 'netflix' not in ET.tostring(feed, encoding='unicode').lower()
    for pair in localize.PAIRS:
        for page in pair:
            text = (ROOT / '_site' / page).read_text()
            links = Links(text).links
            assert 'link-previews.js' in text, page
            assert len([link for link in links if link.get('type') == 'application/rss+xml']) == 1, page
            if not page.startswith('posts/'):
                assert '<!-- post-share -->' not in text
                continue
            url = localize.SITE_URL + '/' + page
            assert 'remember.js' in text and 'cite-this.js' in text
            assert text.count('class="cite-this cite-this--inline"') == 1
            assert 'data-tab-scope="work"' not in text
            assert 'cite-this--mount' not in text
            assert text.count('<!-- post-share -->') == 1
            sharing = next(link for link in links if link.get('href', '').startswith('https://www.linkedin.com/shareArticle?'))
            assert parse_qs(urlsplit(sharing['href']).query)['url'] == [url]
            x_share = next(link for link in links if link.get('href', '').startswith('https://x.com/intent/tweet?'))
            assert parse_qs(urlsplit(x_share['href']).query)['url'] == [url]
            assert 'bi bi-twitter-x' in text and x_share['rel'] == 'noopener noreferrer'
            mail = next(link for link in links if link.get('href', '').startswith('mailto:?subject='))
            assert parse_qs(urlsplit(mail['href']).query)['body'] == [url]
            assert r'\url{' + url + '}' in text, page
            year = '2026' if 'bike-share' in page else '2021'
            assert f'year         = {{{year}}}' in text
    print('Blog features: separate RSS feeds, language discovery, previews, original citation years and exact PT/EN share/citation URLs passed.')


if __name__ == '__main__':
    check()
