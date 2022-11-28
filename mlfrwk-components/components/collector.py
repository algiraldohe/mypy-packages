import sqlalchemy
from configparser import ConfigParser
import pandas as pd
import os


class DataCollector():

    def __init__(self, source, config) -> None:
        self.source = source
        config_path = 'config/config.ini'
        config.read(config_path)

        if source == 'database':
            mandatory = config['DATABASE_CONFIG']['mandatory'].split(",")
            mandatory = {k:v for k,v in config['DATABASE_CONFIG'].items() if (k in mandatory) }
            params = {k:v for k,v in config['DATABASE_CONFIG'].items()}
            empty_parameters = [v for v in mandatory.values()]

            if '' in empty_parameters:
                raise Exception(f"Expected mandatory paramater from {config_path} but '' was received."\
                    f" Check parameters in section [DATABASE_CONFIG]: {mandatory}"
                    )

            url = f"{params['database']}://{params['user_name']}:{params['password']}@{params['host']}/{params['db_name']}"
            self.engine = sqlalchemy.create_engine(url)

        if source == 'file':
            mandatory = config['FILE_SOURCE_CONFIG']['mandatory'].split(",")
            mandatory = {k:v for k,v in config['FILE_SOURCE_CONFIG'].items() if (k in mandatory) }
            params = {k:v for k,v in config['FILE_SOURCE_CONFIG'].items()}
            empty_parameters = [v for v in mandatory.values()]

            

            if '' in empty_parameters:
                raise Exception(f"Expected mandatory paramater from {config_path} but '' was received."\
                    f" Check parameters in section [FILE_SOURCE_CONFIG]: {mandatory}"
                    ) 

            self.filename = params['file_path']
            

    def get_file(self, filename:str = None) -> pd.DataFrame:

        if filename == None:
            filename = self.filename

        sources = dict(xlsx = "pd.read_excel(%s)" , xls = "pd.read_excel(%s)" , csv = "pd.read_csv('%s')" , json = "pd.read_json(%s)")
        file_extension = os.path.splitext(filename)[1][1:]
        dataframe = eval(sources[file_extension]%(filename))

        return dataframe

    def get_sql(self, query:str) -> pd.DataFrame:

        return pd.read_sql(query, con=self.engine)
  
