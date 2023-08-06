from pandas.core import base
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import numpy as np

class CarScraping:
    def __init__(self):
        self.make = []
        self.model = []
        self.fuel_type = []
        self.man_year = []
        self.mileage = []
        self.price = []
        self.gearbox = []
        self.engine_capacity = []
        self.ulez = []
        self.num_doors = []
        self.car_info = []
        self.driver_path = '/usr/local/bin/chromedriver'
        self.driver = webdriver.Chrome(executable_path=self.driver_path)

    def check_exists(self, xpath):
        try:
            self.driver.find_elements_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    def url_generator_car_giant(self, number_of_pages):
        urls = []
        for i in range(number_of_pages):
            urls.append(f'https://www.cargiant.co.uk/search/all/all/page/{i + 1}')
            print(urls[i])
        return urls

    def click_cookie_car_giant(self):
        cookie = self.driver.find_element_by_xpath('//div[@role="dialog"]/div/a')
        cookie.click()

    def click_next_car_giant(self):
        next_button = self.driver.find_element_by_xpath('//div[@class="paging"]/a[@data-paging-pages-template="next"]')
        next_button.click()

    def url_generator_big_motoring_world(self, number_of_pages):
        urls = []
        for i in range(number_of_pages):
            urls.append(f'https://www.bigmotoringworld.co.uk/used/cars/page/{i + 1}/')
        return urls

    def click_cookie_big_motor(self):
        box_xpath = './/*[@class="pop-up__close"]'
        the_box = self.driver.find_element_by_xpath(box_xpath)
        the_box.click()

    def click_next_big_motor(self):
        next_button = self.driver.find_element_by_xpath(
            '//ul[@class="pagination pagination--desktop"]/li[@class="next"]/a')
        next_button.click()

    def big_motoring_scraper(self, page_numbers):
        self.make = []
        self.model = []
        self.fuel_type = []
        self.man_year = []
        self.mileage = []
        self.price = []
        self.gearbox = []
        self.engine_capacity = []
        self.ulez = []
        self.num_doors = []
        self.car_info = []

        urls = self.url_generator_big_motoring_world(page_numbers)
        self.driver.get(urls[0])
        time.sleep(5)

        ulez_only = []

        try:
            self.click_cookie_big_motor()
        except:
            pass

        for i in range(len(urls)):
            cars = []
            make1 = []
            model1 = []
            price1 = []
            ulez1 = []

            self.driver.get(urls[i])
            make1 = self.driver.find_elements_by_xpath('.//span[@class="vehicle__make"]')
            model1 = self.driver.find_elements_by_xpath('.//span[@class="vehicle__model"]')
            price1 = self.driver.find_elements_by_xpath('.//div[@class="price-combined__value"]')
            cars = self.driver.find_elements_by_xpath('.//div[@class="vehicle__technical-data-promoted"]')
            ulez1 = self.driver.find_elements_by_xpath('.//div[@class="vehicle__primary-images-inner"]')

            for j in range(len(cars)):
                self.car_info.append(cars[j].text)
                self.make.append(make1[j].text)
                self.model.append(model1[j].text)
                self.price.append(price1[j].text)
                self.ulez.append(ulez1[j].text)

        # self.driver.close()
        print('Done scraping Big Motoring World!', page_numbers)

        for i in range(len(self.car_info)):
            info = self.car_info[i].splitlines()
            self.fuel_type.append(info[0])
            if info[0] != 'Electric':
                self.engine_capacity.append(info[1])
                self.gearbox.append(info[2])
                self.mileage.append(info[3])
                self.num_doors.append(info[4])
            else:
                self.engine_capacity.append(np.nan)
                self.gearbox.append(info[1])
                self.mileage.append(info[2])
                self.num_doors.append(info[3])
        for i in range(len(self.ulez)):
            info = self.ulez[i].splitlines()
            if 'ULEZ' in info:
                ulez_only.append(1)
            else:
                ulez_only.append(0)

        dictionary = {
            'Make': self.make,
            'Model': self.model,
            'Price': self.price,
            'Mileage': self.mileage,
            'Engine Capacity': self.engine_capacity,
            'Gearbox': self.gearbox,
            'Number of Doors': self.num_doors,
            'ULEZ': ulez_only
        }

        df = pd.DataFrame(dictionary)

        return df

    def car_giant_scraper(self, num_of_pages):
        self.make = []
        self.model = []
        self.fuel_type = []
        self.man_year = []
        self.mileage = []
        self.price = []
        self.gearbox = []
        self.engine_capacity = []
        self.ulez = []
        self.num_doors = []
        self.car_info = []
        base_url = 'https://www.cargiant.co.uk/search/'
        self.driver.get(base_url)
        time.sleep(3)
        self.click_cookie_car_giant()
        for i in range(num_of_pages):
            cars = []
            car_price = []
            cars = self.driver.find_elements_by_xpath('//div[@class="car-listing-item__details split-half"]')
            car_price = self.driver.find_elements_by_xpath('//div[@class="price-block__price"]')
            car_price = car_price[::2]

            for j in range(len(cars)):
                self.car_info.append(cars[j].text)
                self.price.append(car_price[j].text)
            self.click_next_car_giant()

            time.sleep(5)
        print('Done scraping Car Giant! ', num_of_pages, 'Pages')

        for i in range(len(self.car_info)):
            make_model = []
            info1 = self.car_info[i].splitlines()
            make_model.append(info1[0])
            details = info1[2].split()
            self.mileage.append(details[-2])
            self.man_year.append(details[-4])
            self.fuel_type.append(details[-6])
            self.gearbox.append(str(details[-7]).replace(',', ''))
            self.engine_capacity.append(info1[1].split()[0])
            # print(len(info1))
            if info1[-1].split()[0] == 'ULEZ':
                self.ulez.append(1)
            else:
                self.ulez.append(0)

            for j in range(len(make_model)):
                make_model_split = make_model[j].split()
                self.make.append(make_model_split[0])
                self.model.append(make_model_split[1])

        for k in range(len(self.car_info)):
            doors = self.car_info[k].splitlines()[2].split()[0]
            if doors == '3':
                self.num_doors.append('3')
            elif doors == '5':
                self.num_doors.append('5')
            elif doors == 'Coupe,':
                self.num_doors.append('Coupe')
            elif doors == 'Cabriolet':
                self.num_doors.append('Convertible')
            else:
                self.num_doors.append('SUV')

        dictionary = {
            'Make': self.make,
            'Model': self.model,
            'Price': self.price,
            'Mileage': self.mileage,
            'Engine Capacity': self.engine_capacity,
            'Gearbox': self.gearbox,
            'Number of Doors': self.num_doors,
            'ULEZ': self.ulez
        }

        df = pd.DataFrame(dictionary)

        return df