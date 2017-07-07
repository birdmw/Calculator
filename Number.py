# A multi-arm bandit method for creating, sampling,
# and updating a simple number
from random import random, gauss
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


def gauss_function(x, a, x0, sigma):
    return a * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))


def bandit_choice(my_list, key=None):
    if not key:
        running_sum = 0.0
        threshold = random() * float(sum(my_list))
        for i, value in enumerate(my_list):
            running_sum += value
            if running_sum >= threshold:
                return my_list[i]
    else:
        running_sum = 0.0
        threshold = random() * float(sum(item[key] for item in my_list))
        for i, item in enumerate(my_list):
            running_sum += item[key]
            if running_sum >= threshold:
                return my_list[i]


class Number:
    def __init__(self):
        self.latest_bucket = None
        self.buckets = [
            {'min': -1000.0, 'max': 1000.0, 'x_samples': [1, 2, 3, 4, 5, 6, 7, 8, 9],
             'y_samples': [1, 1, 2, 3, 4, 3, 2, 1, 1], 'x_mu': 0.0, 'x_sig': 1.0, 'y_mu': 1.0,
             'y_sig': 1.0}]

    def sample(self):
        bucket = bandit_choice(self.buckets, key='y_mu')
        self.latest_bucket = bucket
        x = gauss(bucket['x_mu'], bucket['x_sig'])
        bucket['x_samples'].append(x)

        print bucket
        return x

    def feedback(self, y_value):
        self.latest_bucket['y_samples'].append(y_value)
        x = np.array(self.latest_bucket['x_samples'])
        y = np.array(self.latest_bucket['y_samples'])
        print x
        print y
        mean = sum(x * y)
        sigma = sum(y * (x - mean) ** 2)
        popt, pcov = curve_fit(gauss_function, x, y)
        plt.plot(x, gauss_function(x, *popt))
        plt.plot(x, y, 'ok')
        plt.show()


# N = Number()
# print N.sample()
# N.feedback(3.)
# print N.buckets


