from hristoScrapper import scraper
import pandas as pd

class test_module_1:

    def big_motor_test():
        test_flag = True
        if(test_flag):
            big_motor_df = scraper.CarScraping.big_motoring_scraper(5)
            scraper.CarScraping.driver.close()
            big_motor_df.to_csv('carpriceprediction/webapp/data/scraped_big_motoring_test.csv')
            return test_flag
        else:
            return False

    def one_page_car_giant():
        test_flag = True
        if(test_flag):
            big_motor_df = scraper.CarScraping.big_motoring_scraper(1)
            scraper.CarScraping.driver.close()
            big_motor_df.to_csv('carpriceprediction/webapp/data/scraped_big_motoring_test.csv')
            return test_flag
        else:
            return False