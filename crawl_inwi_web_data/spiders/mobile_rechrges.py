from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from shutil import which
# from scrapy_selenium import SeleniumRequest
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.selector import Selector
from scrapy.http import Request
from selenium.webdriver.chrome.service import Service

from .recharge_products import RechargeProducts

import scrapy
import logging


class MobileRechargesSel(scrapy.Spider):
    name = "mobile_recharges"
    allowed_domains = ['inwi.ma']
    url = 'https://inwi.ma/particuliers/recharges'

    def __init__(self):
        # chrome_option = Options()
        # chrome_option.add_argument("--headless")
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920,
                                    1080)
        self.driver.get(self.url)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="MuiGrid-root MuiGrid-item mui-style-1wxaqej"]')))
        # sleep(5)
        self.html = self.driver.page_source

    def start_requests(self):
        logging.info('Getting Mobile recharges data')
        yield scrapy.Request(
            url=self.url,
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        response_recharges = Selector(text=self.html)
        cartes = response_recharges.xpath('//div[@class="jss1183"]//div[@class="MuiGrid-root MuiGrid-item '
                                          'mui-style-1wxaqej"]')

        cartes_dict = {}
        for carte in cartes:
            refill_title = carte.xpath('.//span[@class="jss1181"]/text()').getall()
            refill_title = " ".join(refill_title)
            promo_desc = carte.xpath('.//div[@class="MuiGrid-root mui-style-1258v44"]/text()').get()
            refill_type = carte.xpath('.//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-xs-2.3 '
                                      'mui-style-10fuugb"]//span/text()').get()
            refill_desc = carte.xpath('./div/div/div[2]/span/p/text()').get()

            cartes_dict[refill_title] = {
                'refillTitle': refill_title,
                'promoDesc': promo_desc,
                'refillType': refill_type,
                'refillDesc': refill_desc
            }

        cartes_dict['Recharge Dirhams']['productsDetails'] = RechargeProducts(
                                        'https://inwi.ma/particuliers/recharge/promostar/classic'
                                         ).recharge_dirhams_products()
        cartes_dict['Recharge  Appels & SMS']['productsDetails'] = RechargeProducts(
                                        'https://inwi.ma/particuliers/recharge/promostar/appel-sms'
                                        ).recharge_appels_sms_products()
        cartes_dict['Recharge Koulchi']['productsDetails'] = RechargeProducts(
                                        'https://inwi.ma/particuliers/recharge/promostar/appel-sms'
                                        ).recharge_koulchi_products()
        pass


"""
        choisir = self.driver.find_element("xpath",
                                           '/html/body/div/div[4]/div/div[3]/div/div[1]/div/div/div[3]/button')
        choisir.click()
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="r-380"]/div[3]/div[1]/div[3]/span')))
        self.html = self.driver.page_source
        resp2 = Selector(text=self.html)
        test2 = resp2.xpath('//*[@id="r-380"]/div[3]/div[1]/div[3]/span/text()').get()
        self.driver.close()
        self.__init__()

        # for section in sections:
        #     link = section.xpath('.//@href').get()
        #     yield Request(
        #         url=link,
        #         callback=self.save_files
        #     )

        next_page = resp.xpath('//input[@value="Next"][ @disabled="disabled"]')
        while not next_page:
            next = self.driver.find_element_by_xpath(
                '//*[@id="ctl00_bodyMaster_resultListView_resultListViewDataPager"]/input[3]')
            next.click()
            sleep(5)
            self.html = self.driver.page_source
            resp = Selector(text=self.html)
            sections = resp.xpath('//span[@class="smalltext"]/a')
            for section in sections:
                link = section.xpath('.//@href').get()
                yield Request(
                    url=link,
                    callback=self.save_files
                )

            next_page = resp.xpath('//input[@value="Next"][ @disabled="disabled"]')

    def save_files(self, response):
        path = "data/fed/" + response.url.split('/')[-1]
        with open(path, 'wb') as file:
            file.write(response.body)
"""
