import pandas as pd
import numpy as np
import configparser
from types import NoneType
from configparser import ConfigParser
from components.errors import NotConfigFile


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
        config_path = 'config/config.ini'
        config_section = 'DATA_ROLES_CONFIG'
        
        try:
            config.read(config_path)

        except configparser.ParsingError  as e:
            print(f"Not able to read config file {config_path}")
            raise
        
        try:
            if not config._sections:
                raise NotConfigFile(f"ConfigParser is empty, check location and/or content of the file {config_path}")

            self.roles = {k:v for k,v in config[config_section].items()}

        except KeyError:
            print(f"Section {config_section} not found in config file {config_path}")
            raise 

        except NotConfigFile:
            raise

        self.data = data
        self.categorical_cols = []
        self.numeric_cols = []
        self.dimensions = {}
    

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value:pd.DataFrame):
        try:
            dtypes = (NoneType, pd.core.frame.DataFrame, np.ndarray)
            assert isinstance(value, dtypes)
            self._data = value

        except AssertionError:
            error_msg = f"""You are trying to set an invalid type to the data attribute of {self}\
            . Try instead one of the following {dtypes}""".replace("  ", "")
            raise AssertionError(error_msg)