import math
import pprint
from typing import Any
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import zip_longest

from components.container import DataStorageContainer


class StandardOutputViewerMeta(type):
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


class StandardOutputViewer(metaclass=StandardOutputViewerMeta):

    def __init__(self, sections:int, titles:list, overview:bool=True)-> None:
        self.sections = sections
        self.titles = titles
        self.overview = overview
        
    def add_section(self, info:Any, title:str):

        print("\n")
        print(f"{'':=^150}")
        print(f" {title:^150} ")
        print(f"{'':=^150}")
        print("\n")
        print(info)
        print("\n")


    def render_overall_report(self, info:dict):
        if self.overview:
            self.add_section('', "Dataset Overview ")
            DataStorageContainer().data.info()

        for i, element in enumerate(info):
            self.add_section(info[element], self.titles[i])


class GraphViewer():

    def __init__(self) -> None:
        sns.set(style="ticks", palette=('colorblind'),font_scale = 1.00)
        
    
    def plot_single_histogram(self, varname:str, bins_width:int = None) -> None:
        series =  DataStorageContainer().data[varname]

        # Compute optimal number of bins
        if bins_width == None:
            bw = math.ceil(math.sqrt(len(series)))
            
        else:
            bw = bins_width

        plt.figure(figsize=(10,5)) # Make it 14x7 inch
        plt.style.use('seaborn-whitegrid') # nice and clean grid
        plt.hist(series, bins=bw, linewidth=0.5)
        plt.title(f'{varname} Distribution') 
        plt.xlabel(varname) 
        plt.ylabel('Frequency') 
        plt.show()


    def plot_multiple_histograms(self, varnames:list, n_rows:int, n_cols:int):
        data = DataStorageContainer().data
        fig=plt.figure(figsize=(10,5))
        bw = 10#math.ceil(math.sqrt(len(data)))
        for i, var in enumerate(varnames):
            ax=fig.add_subplot(n_rows,n_cols,i+1)
            data[var].hist(bins=bw, ax=ax)
            ax.set_title(var)
        fig.tight_layout()  # Improves appearance a bit.
        plt.show()


    def plot_multiple_hist_class(self, varnames:list, target:str):
        data = DataStorageContainer().data
        target_classes = get_target_classes(data, target)
        
        data_size = data[varnames].shape[1]

        n_rows, n_cols, fig_x, fig_y = set_figure_dimensions(data_size)

        fig=plt.figure(figsize=(fig_x,fig_y))

        for i, var_name in enumerate(varnames):

            # Is not set dinamically for classes != 2
            x = target_classes[0][var_name]
            y = target_classes[1][var_name]

            ax=fig.add_subplot(n_rows,n_cols,i+1)
            plt.hist([x, y], label = ['not churn', 'churn'], density = True)
            ax.set_title(var_name)
            ax.legend(['not churn', 'churn'], loc='best')

        fig.tight_layout()  # Improves appearance a bit.
        plt.show()


    def plot_multiple_barplot(self, varnames:list, target:str) -> None:

        data = DataStorageContainer().data
        data_size = data[varnames].shape[1]

        n_rows, n_cols, fig_x, fig_y = set_figure_dimensions(data_size)
        
        fig=plt.figure(figsize=(fig_x,fig_y))

        for i, var_name in enumerate(varnames):
            
            ax=fig.add_subplot(n_rows,n_cols,i+1)
            sns.barplot(x=data[var_name], y=data[target], errorbar=None)

        fig.tight_layout()  # Improves appearance a bit.
        plt.show()

    def plot_pie_chart(self, varname:str) -> None:
        target_series = DataStorageContainer().data[varname]

        # Compute agg values
        agg_values = target_series.value_counts().to_list()

        fig, ax = plt.subplots()
        ax.pie(agg_values, autopct='%1.1f%%')
        labels = list(target_series.unique())
        plt.legend(labels = labels, loc='lower center', bbox_to_anchor=(0.5, -0.25))
        plt.title(f'Distribution of {target_series.name}')
        plt.show()

        

        
# --------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
def divide_target_class(data:pd.DataFrame, target:str, classes:Any) -> pd.DataFrame:
    class0 = data.loc[data[target] == classes]
    return class0

def set_figure_dimensions(data_shape:int):
    if data_shape % 4 == 0:
        n_cols = 4
    elif data_shape % 3 == 0:
        n_cols = 3
    else :
        n_cols = 2

    n_rows = data_shape / n_cols
    n_rows, n_cols = int(n_rows) , int(n_cols)
    
    if n_rows * n_cols > 9:
        # Need to create another figure and other layout
        figure_x = 15
        figure_y = (figure_x * n_rows)/4 
    
    elif n_rows <= 3:
        figure_x = 15
        figure_y = figure_x/3
        
    # print(f"Figure Size: ({figure_x},{figure_y}) \n Number of Rows: {n_rows} \t Number of Columns: {n_cols}")
    return n_rows, n_cols, figure_x, figure_y


def get_target_classes(data, target):
    num_target_classes = data[target].nunique()
    target_classes = list(data[target].unique())
    df_classes = []
    for i in target_classes:
        df_classes.append(divide_target_class(data, target, i))
        
    return df_classes




    