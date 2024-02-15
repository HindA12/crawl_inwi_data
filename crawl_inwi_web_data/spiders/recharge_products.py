from selenium import webdriver
from scrapy.selector import Selector
from time import sleep


class RechargeProducts:
    def __init__(self, url):
        # chrome_option = Options()
        # chrome_option.add_argument("--headless")
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920,
                                    1080)
        self.driver.get(url)
        sleep(5)
        self.html = self.driver.page_source

    def recharge_dirhams_products(self):
        dict_products = {}
        response = Selector(text=self.html)
        products = response.xpath('//div[@class="MuiGrid-root mui-style-12a3zg4"]/div[@class="jss173"]')
        for prod in products:
            promo_type = prod.xpath('./div[@class="MuiGrid-root mui-style-2vy76"]/text()').get()
            price = prod.xpath('./div[2]//text()').getall()
            price = " ".join(price)
            prod_specs = prod.xpath('./div[@class="jss178"]/div')
            is_promo = False
            if promo_type:
                is_promo = True
            dict_products[price + promo_type] = {
                'promoType': promo_type,
                'price': price,
                'isPromo': is_promo,
            }
            dict_products[price + promo_type]['productSpecs'] = []
            for spec in prod_specs:
                value = spec.xpath('./div[@class="jss184 special"]/span[1]//text()').get()
                promo_value = spec.xpath('./div[@class="jss184 special"]/span[2]//text()').get()
                validity = spec.xpath('./div[@class="jss185 "]//text()').getall()
                validity = " ".join(validity)
                dict_products[price + promo_type]['productSpecs'].append({
                    'value': value,
                    'promoValue': promo_value,
                    'validity': validity
                })

        self.driver.close()
        return dict_products

    def recharge_appels_sms_products(self):
        dict_products = {}
        response = Selector(text=self.html)
        products = response.xpath('//div[@class="MuiGrid-root mui-style-12a3zg4"]/div[@class="jss157"]')
        for prod in products:
            promo_type = prod.xpath('.//div[@class="MuiGrid-root mui-style-2vy76"]/text()').get()
            value = None
            if promo_type:
                price = prod.xpath('./div[2]//text()').getall()
                is_promo = True
            else:
                price = prod.xpath('./div[1]//text()').getall()
            price = " ".join(price)
            span = prod.xpath('./div[@class="jss162"]/div/div[2]/span')
            if 1 == len(span):
                value = span.xpath('.//text()').get()
                promo_value = None
            elif 2 == len(span):
                value = prod.xpath('./div[@class="jss162"]/div/div[2]/span[1]//text()').get()
                promo_value = prod.xpath('./div[@class="jss162"]/div/div[2]/span[2]//text()').get()
            validity = prod.xpath('.//div[@class="jss169 "]//text()').getall()
            validity = " ".join(validity)
            dict_products[price] = {
                'isPromo': is_promo,
                'value': value,
                'promoValue': promo_value,
                'validity': validity,
                'price': price
            }

        self.driver.close()
        return dict_products

    def recharge_koulchi_products(self):
        dict_products = {}
        response = Selector(text=self.html)
        products = response.xpath('/html/body/div/div[4]/div[2]/div[2]/div/div')
        for product in products:
            promo_type = product.xpath('./div[@class="MuiGrid-root mui-style-2vy76"]/text()').get()
            if promo_type != None:
                price = product.xpath('./div[2]//text()').getall()
                is_promo = True
                offres = product.xpath('./div[3]/div')
            else:
                price = product.xpath('./div[1]//text()').getall()
                is_promo = False
                offres = product.xpath('./div[2]/div')
            price = " ".join(price)
            choix = []
            for offre in offres:
                value = offre.xpath('./div[2]/span/p//text()').get()
                choix.append(value)
            offers_types = ['Appels', 'Internet', 'SMS', 'Appels Internationaux']
            values = dict(zip(offers_types, choix))
            validity = offres[0].xpath('./div[3]/span//text()').getall()[1]
            dict_products[price] = {
                'isPromo': is_promo,
                'Values': values,
                'Validity': validity,
                'Price': price
            }

        self.driver.close()
        return dict_products

    def recharge_appels_ilimités_inwi(self):
        dict_products = {}
        response = Selector(text=self.html)
        products = response.xpath('/html/body/div/div[4]/div[2]/div[2]/div/div')
        for product in products:
            price = product.xpath('./div[1]//text()').getall()
            price = " ".join(price)
            offers = product.xpath('./div[2]/div')
            values = []
            for offer in offers:
                values.append(offer.xpath('./div[2]/span/p//text()').get())
            values[0] = 'Appels ' + values[0]
            validity = offers[0].xpath('./div[3]/span//text()').getall()
            validity = " ".join(validity)
            dict_products[price] = {
                'Price': price,
                'Values': values,
                'Validity': validity
            }

        self.driver.close()
        return dict_products

    def recharge_roaming(self):
        dict_products = {}
        response = Selector(text=self.html)
        products = response.xpath('/html/body/div/div[4]/div[2]/div[2]/div/div')
        for product in products:
            promo_type = product.xpath('./div[@class="MuiGrid-root mui-style-2vy76"]//text()').get()
            if promo_type != None:
                price = product.xpath('./div[2]//text()').getall()
                is_promo = True
                offers = product.xpath('./div[3]/div')
            else:
                price = product.xpath('./div[1]//text()').getall()
                is_promo = False
                offers = product.xpath('./div[2]/div')
            price = " ".join(price)
            values = []
            for offer in offers:
                value = offer.xpath('./div[2]/span/p//text()').getall()
                value = " ".join(value)
                values.append(value)
            if len(values) == 1:
                values_dict = dict(zip(['Internet'], values))
            elif len(values) == 3:
                values_dict = dict(zip(['Appels', 'Internet', 'SMS'], values))

            validity = offers[0].xpath('./div[3]/span//text()').getall()
            validity = " ".join(validity)

            dict_products[price] = {
                'isPromo': is_promo,
                'promoType': promo_type,
                'Values': values_dict,
                'Validity': validity,
                'Price': price
            }

        self.driver.close()

# if __name__ == "__main__":
#     RechargeProducts('https://inwi.ma/particuliers/recharge/promostar/appel-sms').recharge_appels_sms_products()
