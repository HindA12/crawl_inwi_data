import scrapy
import logging
import json


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class MobileRecharges(scrapy.Spider):
    name = "mobile_recharges_"
    allowed_domains = ['inwi.ma']
    url = 'https://inwi.ma/particuliers/recharge/promostar/classic'
    cookies = {
        '_gcl_aw': 'GCL.1700752322.CjwKCAiAjfyqBhAsEiwA-UdzJC2U7OeSphbSmmFy5valx4gN5PmJMAK3BpukFEIkgJw5ASF9QXz-3BoCWtcQAvD_BwE',
        '_gcl_au': '1.1.1194454485.1700752322',
        '_ga': 'GA1.1.1479909964.1700752322',
        '_tt_enable_cookie': '1',
        '_ttp': 'LlMqULlKhuYq2waBLGgIwsobAR8',
        '_hjSessionUser_2973411': 'eyJpZCI6IjA3NGRjODliLWFhM2EtNThiOC04NWUzLTUxMTJmMjg2NjhhNyIsImNyZWF0ZWQiOjE3MDA3NTIzMjE5NzAsImV4aXN0aW5nIjp0cnVlfQ==',
        'dtCookie': 'v_4_srv_1_sn_3B77FB299E9802DA626D17982B6FD656_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0',
        'OClmoOot': 'AyIURH-NAQAA8kNfkkfX7HebcPg2cirT8iYLTDPQxkftOVEOjQa3fPt3wAxjASmJD3GuclIDwH8AAEB3AAAAAA|1|0|43b2ab0f729bdeb59637d582865ae729e291fced',
        '_hjSession_2973411': 'eyJpZCI6ImZhMzhkY2E4LWQ5MzEtNDRiMC1hMDg4LTgzYjk5MDlkYmY2OCIsImMiOjE3MDc0NzM5NjMyMzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=',
        'TS01fad0f5': '018e1322efa336e1c084d3ace46fd13c09884f173289528a6e3f974c67ca761699e7068e2e8344aac389e2282d03d6fb86f473c77998991a71702f0e63a20dd8bdde02f550',
        '_ga_LK3B9T432N': 'GS1.1.1707473963.15.1.1707474448.55.0.0',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': '_gcl_aw=GCL.1700752322.CjwKCAiAjfyqBhAsEiwA-UdzJC2U7OeSphbSmmFy5valx4gN5PmJMAK3BpukFEIkgJw5ASF9QXz-3BoCWtcQAvD_BwE; _gcl_au=1.1.1194454485.1700752322; _ga=GA1.1.1479909964.1700752322; _tt_enable_cookie=1; _ttp=LlMqULlKhuYq2waBLGgIwsobAR8; _hjSessionUser_2973411=eyJpZCI6IjA3NGRjODliLWFhM2EtNThiOC04NWUzLTUxMTJmMjg2NjhhNyIsImNyZWF0ZWQiOjE3MDA3NTIzMjE5NzAsImV4aXN0aW5nIjp0cnVlfQ==; dtCookie=v_4_srv_1_sn_3B77FB299E9802DA626D17982B6FD656_perc_100000_ol_0_mul_1_app-3Aea7c4b59f27d43eb_0; OClmoOot=AyIURH-NAQAA8kNfkkfX7HebcPg2cirT8iYLTDPQxkftOVEOjQa3fPt3wAxjASmJD3GuclIDwH8AAEB3AAAAAA|1|0|43b2ab0f729bdeb59637d582865ae729e291fced; _hjSession_2973411=eyJpZCI6ImZhMzhkY2E4LWQ5MzEtNDRiMC1hMDg4LTgzYjk5MDlkYmY2OCIsImMiOjE3MDc0NzM5NjMyMzksInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; TS01fad0f5=018e1322efa336e1c084d3ace46fd13c09884f173289528a6e3f974c67ca761699e7068e2e8344aac389e2282d03d6fb86f473c77998991a71702f0e63a20dd8bdde02f550; _ga_LK3B9T432N=GS1.1.1707473963.15.1.1707474448.55.0.0',
        'Referer': 'https://inwi.ma/particuliers/recharges',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    def start_requests(self):
        logging.info('Getting Mobile recharges data')
        yield scrapy.Request(url=self.url,
                             callback=self.parse,
                             cookies=self.cookies,
                             headers=self.headers
        )

    def parse(self, response, **kwargs):
        test = response.xpath('//*[@id="r-380"]/div[3]/div[1]/div[2]/span[2]/p/span/strong/text()').get()

        if 404 == response.status:
            logging.warning(f'Mobile recharges page not found')
        if 200 != response.status:
            logging.warning(f'Response != 200: {response.status}, message: {response.body.decode()}')
        data = response.xpath('//*[@id="__NEXT_DATA__"]').get()

        json_data = json.loads(data)['props']['pageProps']['data']


