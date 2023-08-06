import csv
from sqlalchemy import create_engine
import pandas as pd

class rds_upload:
    def __init__(self):
        self.DATABASE_TYPE = 'postgresql'
        self.DBAPI = 'psycopg2'
        self.ENDPOINT = 'aicoredb.ciff0yoegxyv.us-east-2.rds.amazonaws.com'  # Change it for your AWS endpoint
        self.USER = 'postgres'
        self.PASSWORD = 'Anpollocpi'
        self.PORT = 5432
        self.DATABASE = 'postgres'

    def build_engine(self):
        engine = create_engine(
            f"{self.DATABASE_TYPE}+{self.DBAPI}://{self.USER}:{self.PASSWORD}@{self.ENDPOINT}:{self.PORT}/{self.DATABASE}")

        return engine
