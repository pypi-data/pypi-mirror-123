import scraping
import pandas as pd
from .scraping import CarScraping

if __name__ == "__main__":

    scraping = CarScraping()
    giant_df = scraping.car_giant_scraper(50)
    big_motor_df = scraping.big_motoring_scraper(77)
    main_df = pd.concat([giant_df, big_motor_df], ignore_index=True)
    main_df.to_csv('scraped_data.csv')