import numpy as np
import matplotlib.pyplot as plt

# Create a sequence of numbers going from 0 to 100 in intervals of 0.5
start_val = 0
stop_val = 100
n_samples = 200
X = np.linspace(start_val, stop_val, n_samples)

params = np.array([2, -5])

# Build the vector [x, 1] for each x value so we can compute P · [x, 1]
X_with_bias = np.column_stack((X, np.ones_like(X)))

# y = P · [x, 1] = m*x + b
f_x = X_with_bias @ params

# Plot the line
plt.plot(X, f_x, color='blue', label='f(x) = P · [x, 1]')
plt.axhline(0, color='black', linewidth=0.8)
plt.axvline(0, color='black', linewidth=0.8)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Linear Function from Parameter Vector')
plt.grid(True)
plt.legend()
plt.show()