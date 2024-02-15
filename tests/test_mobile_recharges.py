import unittest
# from scrapyproject.spiders import osdir_spider
from responses import fake_response_from_file
from crawl_inwi_web_data.spiders import mobile_recharges
from unittest.mock import patch, MagicMock


class MobileRechargesTest(unittest.TestCase):

    def setUp(self):
        self.spider = mobile_recharges.MobileRecharges()

    # def _test_item_results(self, results, expected_length):
    #     count = 0
    #     permalinks = set()
    #     for item in results:
    #         self.assertIsNotNone(item['content'])
    #         self.assertIsNotNone(item['title'])
    #     self.assertEqual(count, expected_length)

    @patch('pathlib.Path.write_bytes', MagicMock())
    def test_parse(self):
        results = self.spider.parse(fake_response_from_file('quotes-1.html'))
        # self._test_item_results(results, 10) \
        self.assertEqual(None, results)
