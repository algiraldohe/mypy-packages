import sqlalchemy
from configparser import ConfigParser
import pandas as pd
import os


class DataCollector():

    def __init__(self, source, config) -> None:
        self.source = source
        config.read('config/data.ini')

        if source == 'database':
            instance = config['DATABASE_CONFIG']['database']
            user = config['DATABASE_CONFIG']['user_name']
            password = config['DATABASE_CONFIG']['password']
            host = config['DATABASE_CONFIG']['host']
            port = config['DATABASE_CONFIG']['port']
            database = config['DATABASE_CONFIG']['db_name']
            url = f"{instance}://{user}:{password}@{host}/{database}"
            self.engine = sqlalchemy.create_engine(url)

        if source == 'file':
            self.filename = config['FILE_SOURCE_CONFIG']['file_path']
            

    def get_file(self, filename:str = None) -> pd.DataFrame:

        if filename == None:
            filename = self.filename

        sources = dict(xlsx = "pd.read_excel(%s)" , xls = "pd.read_excel(%s)" , csv = "pd.read_csv('%s')" , json = "pd.read_json(%s)")
        file_extension = os.path.splitext(filename)[1][1:]
        dataframe = eval(sources[file_extension]%(filename))

        return dataframe

    def get_sql(self, query:str) -> pd.DataFrame:

        return pd.read_sql(query, con=self.engine)
  
