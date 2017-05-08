# coding: utf-8
import os
import urllib3._collections
import mock
import unittest
from io import BytesIO

class ScraperTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__), 'index.html'), 'rb') as s:
            cls.index_html = s.read()
        with open(os.path.join(os.path.dirname(__file__), 'search_result.html'), 'rb') as s:
            cls.search_result_html = s.read()
        with open(os.path.join(os.path.dirname(__file__), 'detail.html'), 'rb') as s:
            cls.detail_html = s.read()

    def test_fetch_categories_without_charset(self):
        from ..scraper import Scraper, ScraperError
        requester = mock.Mock(
            request=mock.Mock(
                return_value=mock.MagicMock(
                    headers=urllib3._collections.HTTPHeaderDict({
                        'Content-Type': 'text/html'
                        }),
                    release_conn=mock.Mock(),
                    wraps=BytesIO(self.index_html)
                    )
                )
            )
        scraper = Scraper(requester=requester)
        with self.assertRaises(ScraperError):
            scraper.fetch_categories()

    def test_fetch_categories_with_charset(self):
        from ..scraper import Scraper
        requester = mock.Mock(
            request=mock.Mock(
                return_value=mock.MagicMock(
                    headers=urllib3._collections.HTTPHeaderDict({
                        'Content-Type': 'text/html; cHaRSeT=UTF-8'
                        }),
                    release_conn=mock.Mock(),
                    wraps=BytesIO(self.index_html)
                    )
                )
            )
        scraper = Scraper(requester=requester)
        categories = scraper.fetch_categories()
        self.assertEqual(len(categories), 223)

    def test_fetch_search_result(self):
        from ..scraper import Scraper
        requester = mock.Mock(
            request=mock.Mock(
                return_value=mock.MagicMock(
                    headers=urllib3._collections.HTTPHeaderDict({
                        'Content-Type': 'text/html; charset=UTF-8'
                        }),
                    release_conn=mock.Mock(),
                    wraps=BytesIO(self.search_result_html)
                    )
                )
            )
        scraper = Scraper(requester=requester)
        items, next_page = scraper.fetch_items_in_search_page('')
        self.assertEqual(len(items), 20)
        self.assertEqual(next_page, 'http://example.com/next')

    def test_fetch_info_in_detail_page(self):
        from ..scraper import Scraper
        requester = mock.Mock(
            request=mock.Mock(
                return_value=mock.MagicMock(
                    headers=urllib3._collections.HTTPHeaderDict({
                        'Content-Type': 'text/html; charset=UTF-8'
                        }),
                    release_conn=mock.Mock(),
                    wraps=BytesIO(self.detail_html)
                    )
                )
            )
        scraper = Scraper(requester=requester)
        detail = scraper.fetch_info_in_detail_page('http://example.com/')
        self.assertEqual(len(detail[u'images']), 1)
        self.assertEqual(detail[u'images'][0][u'title'], u'タイトル')
        self.assertEqual(detail[u'images'][0][u'url'], u'http://example.com')
        self.assertEqual(detail[u'description'], u'イラストの説明文')
        self.assertEqual(detail[u'title'], u'イラストのタイトル')

