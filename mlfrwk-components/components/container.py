import pandas as pd
from configparser import ConfigParser


class DataStorageContainerMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]



class DataStorageContainer(metaclass=DataStorageContainerMeta):
    
    def __init__(self, config:ConfigParser, data:pd.DataFrame = None) -> None:
        config.read('config/data.ini')
        self.data = data
        self.data_id = config['FILE_SOURCE_CONFIG']['id_columns']
        self.data_datetime = config['FILE_SOURCE_CONFIG']['datetime_columns']
        self.data_target = config['FILE_SOURCE_CONFIG']['target']
        self.categorical_cols = []
        self.numeric_cols = []
        self.dimensions = {}

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value:pd.DataFrame):
        self._data = value