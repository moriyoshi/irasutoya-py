# coding: utf-8

import cgi
import operator
import itertools
from lxml import etree
import six
import urllib3


class ScraperError(Exception):
    pass


def extract_text(n):
    def _(r, n):
        if n.text is not None:
            r.append(n.text)
        for cn in n.iterchildren():
            _(r, cn)
        if n.tail is not None:
            r.append(n.tail)
    r = []
    _(r, n)
    return u''.join(r)


class Scraper(object):
    allowed_content_types = [
        'text/html',
        'application/xhtml+xml',
        ]

    def __init__(self, index_page_url='http://www.irasutoya.com/', requester=urllib3.PoolManager(), parser_factory=etree.HTMLParser):
        self.index_page_url = index_page_url
        self.requester = requester
        self.parser_factory = parser_factory

    def _fetch(self, method, url, fields=None, headers=None, **kwargs):
        try:
            resp = self.requester.request(method, url, fields, headers, preload_content=False, **kwargs)
            content_type, params = cgi.parse_header(resp.headers['Content-Type'])
            if content_type not in self.allowed_content_types:
                raise ScraperError('{method} {url} resulted in unsupported content type: {content_type}'.format(method=method, url=url, content_type=content_type))
            encoding = params.get('charset')
            parser = self.parser_factory(encoding=encoding)
            return etree.parse(resp, parser)
        finally:
            resp.release_conn()

    def fetch_categories(self):
        t = self._fetch('GET', self.index_page_url)
        ul = t.xpath(u'//*[@id="sidebar"]/*/h2[text()="詳細カテゴリー"]/following-sibling::*/ul')
        if len(ul) == 0:
            raise ScraperError('unexpected HTML structure')
        lis = ul[0].findall('li')
        return {
            anchor.text: anchor.get(u'href')
            for anchor in (li.find(u'a') for li in lis)
            }

    def fetch_items_in_search_page(self, url):
        t = self._fetch('GET', url) 
        anchors = t.xpath(u'//*[@id="main"]//*[contains(@class, "blog-posts")]/*/h2/../../*[@class="date-outer"]//*[@class="box"]/*[contains(@class, "boxmeta")]//h2/a')
        next_page_anchor = t.xpath(u'//*[@id="main"]//*[@id="navigation"]//*[contains(@id, "-pager-older-link")]/a')
        items = [
            {
                u'title': anchor.text,
                u'url': anchor.get(u'href'),
                }
            for anchor in anchors
            ]
        return items, (next_page_anchor[0].get(u'href') if next_page_anchor else None)

    def fetch_all_items_starting_from(self, url, with_details=True):
        items = []
        while url is not None: 
            items_for_page, url = self.fetch_items_in_search_page(url)
            if with_details:
                for item in items_for_page:
                    item.update(self.fetch_info_in_detail_page(item[u'url']))
            items.extend(items_for_page)
        return items

    def fetch_info_in_detail_page(self, url):
        t = self._fetch('GET', url) 
        post = t.xpath(u'//*[@id="main"]//*[@id="post"]')
        if len(post) == 0:
            raise ScraperError('unexpected HTML structure')
        title_node = post[0].find(u'./*[@class="title"]')
        if title_node is None:
            raise ScraperError('unexpected HTML structure')
        entry_node = post[0].find(u'*[@class="entry"]')
        if entry_node is None:
            raise ScraperError('unexpected HTML structure')
        images = entry_node.xpath(u'.//img/parent::a')
        if len(images) == 0:
            raise ScraperError('unexpected HTML structure')
        description = u''.join(
            itertools.takewhile(
                operator.truth,
                (extract_text(c).strip() for c in reversed(entry_node.getchildren()) if c.get(u'class') != u'clear')
                )
            )

        title = extract_text(title_node).strip()

        return {
            u'title': title,
            u'images': [
                {
                    u'url': image.get(u'href'),
                    u'title': image.find(u'img').get(u'alt'),
                    }
                for image in images
                ],
            u'description': description
            }



