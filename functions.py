from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

california = fetch_california_housing()

data = pd.DataFrame(data=california.data, columns=california.feature_names) # создаём таблицу
data['PRICE'] = california.target

def gisto(item, x, y='Price'):
    plt.figure()
    plt.hist(data[item], ec='black', color='#00796b')
    plt.xlabel(x)
    plt.ylabel(y)
    plt.show()

def gisto2(item, x, y='Price'):
    frequency = data[item].value_counts()
    plt.figure()
    plt.xlabel(x)
    plt.ylabel(y)
    plt.bar(frequency.index, height=frequency)
    plt.show()

