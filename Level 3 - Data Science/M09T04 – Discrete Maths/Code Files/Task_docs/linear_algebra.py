import numpy as np
import matplotlib.pyplot as plt

# Create a sequence of numbers going from 0 to 100 in intervals of 0.5
start_val = 0
stop_val = 100
n_samples = 200
X = np.linspace(start_val, stop_val, n_samples)

params = np.array([2, -5])

"""
-----------------
Task 1
------------------

Plot f(x) = P.X, where p is your params
"""