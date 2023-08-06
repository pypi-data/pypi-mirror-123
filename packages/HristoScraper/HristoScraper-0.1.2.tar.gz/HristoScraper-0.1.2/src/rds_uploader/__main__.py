from rds_module_1 import rds_upload
import pandas as pd

if __name__ == "__main__":
    rds = rds_upload()  #creating an object of the rds upload class (module)
    engine = rds.build_engine() #using the build engine method of the rds_upload class
    engine.connect()
    data = pd.read_csv('./scraped_data.csv')
    #print(data.head())

    data.to_sql('scrapped_data', engine, if_exists='replace')
    print('Upload to RDS complete!')
    # df = pd.read_sql_table('scrapped_data', engine)
    # print(df.head())