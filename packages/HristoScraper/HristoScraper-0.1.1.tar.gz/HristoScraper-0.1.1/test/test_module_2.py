from hristoScrapper import scraper
import pandas as pd

class test_module_2:

    def cargiant_test():
        test_flag = True
        if(test_flag):
            giant_df = scraper.CarScraping.car_giant_scraper(5)
            scraper.CarScraping.driver.close()
            giant_df.to_csv('carpriceprediction/webapp/data/scraped_cargiant_test.csv')
            return test_flag
        else:
            return False

    def one_page_car_giant():
        test_flag = True
        if(test_flag):
            giant_df = scraper.CarScraping.car_giant_scraper(1)
            scraper.CarScraping.driver.close()
            giant_df.to_csv('carpriceprediction/webapp/data/scraped_1page_cargiant_test.csv')
            return test_flag
        else:
            return False