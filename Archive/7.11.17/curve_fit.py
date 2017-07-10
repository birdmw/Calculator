import numpy as np
from scipy.stats import randint as sp_randint
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
from scipy.optimize import curve_fit
import inspect
from random import random


def func(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
ydata = [0, 0, 1, 1, 2, 3, 3.5, 3, 2, 1, 1, 0, 0]

args = set(inspect.getargspec(gauss_function).args) - {'x'}
vars = curve_fit(gauss_function, xdata, ydata)

print vars
