# A multi-arm bandit method for creating, sampling,
# and updating a simple number
import math
from math import sqrt
import random

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error


def bandit_choice(my_list, amp=1., key=None):
    if not key:
        running_sum = 0.0
        threshold = random.random() * float(sum([item ** amp for item in my_list]))
        for i, value in enumerate(my_list):
            running_sum += value ** amp
            if running_sum >= threshold:
                return my_list[i]
    else:
        running_sum = 0.0
        threshold = random.random() * float(sum([item[key] ** amp if item[key] else 0.5 for item in my_list]))
        for i, item in enumerate(my_list):
            if item[key]:
                running_sum += item[key] ** amp
            else:
                running_sum += 0.5 ** amp
            if running_sum >= threshold:
                return my_list[i]


def rmse(x, arr):
    x_arr = [x] * int(np.array(arr).size)
    return sqrt(mean_squared_error(x_arr, arr))


class Number:
    def __init__(self, min_range, max_range, bucket_count):
        self.max_samples = 20
        bucket_size = (max_range - min_range) / float(bucket_count)
        self.buckets = []
        i_min, i_max = min_range, min_range + bucket_size
        for _ in range(bucket_count):
            self.buckets.append(
                {'min': i_min, 'max': i_max, 'last_sample': None, 'x_samples': [], 'scores': [], 'avg': None})
            i_min += bucket_size
            i_max += bucket_size
        self.latest_bucket = None

    def __call__(self):
        bucket = bandit_choice(self.buckets, key='avg')
        self.latest_bucket = bucket
        bucket['last_sample'] = random.uniform(bucket['min'], bucket['max'])
        return bucket['last_sample']

    def feedback(self, score):
        lb = self.latest_bucket
        lb['x_samples'].append(lb['last_sample'])
        x, y = lb['x_samples'], lb['scores']
        y.append(score)
        x, y = x[-self.max_samples:], y[-self.max_samples:]
        self.latest_bucket['avg'] = sum(y) / float(len(y))

    def redraw(self):
        plt.clf()
        for bucket in self.buckets:
            x_0, x_1, y = bucket['min'], bucket['max'], bucket['avg']
            plt.plot([x_0, x_1], [y, y], 'k-', lw=3)
        plt.pause(0.01)

    def __str__(self):
        return str(self())


def judge(sample):
    return ((math.sin(sample * 2) + 1.0) / 2.0) ** 4


def judge2(sample):
    return ((math.sin(sample / 2) + 1.0) / 2.0) ** 4


def draw(n, fxn):
    for bucket in n.buckets:
        x_0, x_1, y = bucket['min'], bucket['max'], bucket['avg']
        plt.plot([x_0, x_1], [y, y], 'k-', lw=3)
    x, y = [], []
    for i in range(10):
        sample = n()
        score = fxn(sample)
        n.feedback(score)
        x.append(sample)
        y.append(score)
        plt.plot(x, y, 'ro')
    plt.show()


def test():
    n = Number(min_range=-10, max_range=10, bucket_count=100)
    for i in range(1000):
        sample = n()
        n.feedback(judge(sample))

    draw(n, judge)

    for i in range(1000):
        sample = n()
        n.feedback(judge2(sample))

    draw(n, judge2)


if __name__ == "__main__":
    test()
