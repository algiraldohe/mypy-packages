from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from configparser import ConfigParser
import pandas as pd

# from components.collector import DataCollector
# from components.processor import DataProcessor
from components.container import DataStorageContainer
from components.viewer import StandardOutputViewer


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def add_numerical_info(self) -> None:
        pass

    @abstractmethod
    def add_categorical_info(self) -> None:
        pass


class ReportBuilder1(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._product = ReportOverview()

    @property
    def product(self) -> ReportOverview:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different products that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another product.
        That's why it's a usual practice to call the reset method at the end of
        the `getProduct` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        product = self._product
        self.reset()
        return product

    def add_numerical_info(self) -> None:
        container = DataStorageContainer()
        self._product.add("PartA1")

        if not container.numeric_cols:
            message = f"There are not columns to compute the overview information on"
            #print(f"{'':.^150}")
            print(f" WARNING: {message}{'':.^125} ")
            #print(f"{'':.^150}")
            return None

        parameters = {
            'functions':dict(Count = 'count()'
            , Missing = 'isna().sum()', Mean = 'mean()'
            , Std_Dev = 'std()', Min = 'min()'
            , Max = 'max()', Median = 'median()'
            ),
            'keyname': 'numerical_info',
            'title': "\tNumeric Variables Summary\t",
        }

        self._product.set_attributes(attributes=parameters)

        self._product.generate_info(functions=parameters['functions'], key=parameters['keyname'], columns=container.numeric_cols)
        # self._product.display_info()


    def add_categorical_info(self) -> None:
        container = DataStorageContainer()
        self._product.add("PartB1")
        parameters = {
            'functions': dict(Levels = 'nunique()', Count = 'count()', Missing = 'isna().sum()', Mode = 'mode()[0]')
            , 'keyname': 'categorical_info'
            , 'title': "\tCategorical Variables Summary\t"
        }

        if not container.categorical_cols:
            message = f"There are not columns to compute the overview information on"
            #print(f"{'':.^150}")
            print(f" WARNING: {message}{'':.^125} ")
            #print(f"{'':.^150}")
            return None

        self._product.set_attributes(attributes=parameters)

        self._product.generate_info(functions=parameters['functions'], key=parameters['keyname'], columns=container.categorical_cols)
        #self._product.display_info()



class ReportOverview():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self) -> None:
        container = DataStorageContainer()
        self.parts = []
        self.titles = []
        self.information = {}

    def add(self, part: Any) -> None:
        self.parts.append(part)
        

    def list_parts(self) -> None:
        print(self.parts)

    def set_attributes(self, attributes:dict):
        self.information[attributes['keyname']] = pd.DataFrame()
        self.titles.append(attributes['title'])

    def generate_info(self, functions:dict, key:str, columns:list) -> None:
        container = DataStorageContainer()

        for function in functions.values():

            expression = f'x.{function}'
            if function != None:  
                num_data = container.data[columns].apply(lambda x: eval(expression), axis=0)
                self.information[key] = pd.concat([self.information[key] , num_data], axis=1)
        
            continue
        self.information[key] = self.information[key].set_axis(list(functions.keys()), axis=1)
    
    def display_info(self):
             std_output = StandardOutputViewer(sections=len(self.information), titles=self.titles)
             std_output.render_overall_report(info=self.information)
        

    