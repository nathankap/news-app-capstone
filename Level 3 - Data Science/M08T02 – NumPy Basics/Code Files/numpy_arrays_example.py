"""
Demonstration of NumPy array creation, indexing, and attributes.
This script shows various ways to create and manipulate NumPy arrays
of different dimensions.
"""

import numpy as np

# Set random seed for reproducible results
np.random.seed(0)

# Create random arrays of different dimensions
# 1D array: vector with 6 elements
x1 = np.random.randint(10, size=6)
# 2D array: 3 rows x 4 columns matrix
x2 = np.random.randint(10, size=(3, 4))
# 3D array: 3 matrices of 4x5 elements
x3 = np.random.randint(10, size=(3, 4, 5))

# Demonstrate 1D array operations
print('One-dimensional array (x1):')
print(x1)

print('\nIndexing 1D array:')
print(f'First element (x1[0]): '
      f'{x1[0]}')  # Access first element
print(f'Last element (x1[-1]): '
      f'{x1[-1]}')  # Access last element using negative indexing

# Demonstrate 2D array operations
print('\nTwo-dimensional array (x2):')
print(x2)

print('\nIndexing 2D array:')
# Access element at last column of third row
print(f'Element at position (2,-1): {x2[2, -1]}')

# Demonstrate 3D array operations
print('\nThree-dimensional array (x3):')
print(x3)

# Display array attributes
print('\nArray Attributes for x3:')
# Number of array axes (dimensions)
print(f'Number of dimensions (ndim): {x3.ndim}')
# Tuple of array dimensions (n,m,p)
print(f'Array shape: {x3.shape}')
# Total number of elements in the array
print(f'Total elements (size): {x3.size}')
# Type of elements in the array
print(f'Data type (dtype): {x3.dtype}')
# Memory size of each array element
print(f'Size of each element: {x3.itemsize} bytes')
# Total memory used by the array
print(f'Total array size: {x3.nbytes} bytes')
