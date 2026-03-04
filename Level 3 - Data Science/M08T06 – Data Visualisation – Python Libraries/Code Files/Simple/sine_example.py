import matplotlib.pyplot as plt
import numpy as np

# Generate 100 evenly spaced values for the x-axis
x = np.linspace(0, 100, 100)

# Calculate sine of each x value for the y-axis
y = np.sin(x)

# Plot the x and y values
plt.plot(x, y, label="sine")

# Add a title
plt.title("My first matplotlib sine graph")

# Show the plot
plt.show()
