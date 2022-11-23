import pandas as pd
from configparser import ConfigParser
import warnings
from typing import Any
from itertools import zip_longest

from components.viewer import StandardOutputViewer
from components.container import DataStorageContainer
from components.reporter import ReportBuilder1


class DataProcessor():

    def __init__(self) -> None:
        pass


    def split_attributes(self) -> None:
        container = DataStorageContainer()
        data = container.data
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        data = data.drop(columns=[col for col in [container.data_id, container.data_datetime, container.data_target] if col != ''])
        container.categorical_cols = list(data.select_dtypes(exclude=numerics).columns)
        container.numeric_cols = list(data.select_dtypes(exclude=['object']).columns)


    def get_data_dimension(self) -> dict:
        container = DataStorageContainer()
        dimensions = dict(Rows = 0, Columns = 0, Attributes = '')

        dimensions['Rows'] = container.data.shape[0]
        dimensions['Columns'] = container.data.shape[1]
        dimensions['Attributes'] = container.data.columns.to_list()

        return dimensions


    def summary(self):
        builder = ReportBuilder1()
        builder.add_numerical_info()
        builder.add_categorical_info()
        builder.product.display_info()
        
        





        



    

