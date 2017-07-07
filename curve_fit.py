import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


# Generate some data for this demonstration.
data = norm.rvs(3, 2.5, size=50)
print data

# Fit a normal distribution to the data:
mu, std = norm.fit(data)
print mu, std