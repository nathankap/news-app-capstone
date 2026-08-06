import numpy as np

# ============================================================
# i. Why doesn't this create a 2D array?
#
# np.array((1,0,0), (0,1,0), (0,0,1), dtype=float)
#
# np.array() accepts ONE main object containing the data.
# The rows must be placed inside a single list or tuple.
# ============================================================

# Correct way:
identity = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
], dtype=float)

print("i.")
print(identity)
print()

# ============================================================
# ii. Difference between:
# a = np.array([0,0,0])
# a = np.array([[0,0,0]])
#
# The first is a 1-dimensional array with shape (3,)
# The second is a 2-dimensional array with shape (1,3)
# ============================================================

a = np.array([0, 0, 0])
b = np.array([[0, 0, 0]])

print("ii.")
print(a)
print("Shape:", a.shape)

print(b)
print("Shape:", b.shape)
print()

# ============================================================
# iii. Create the array
# ============================================================

array = np.linspace(1, 48, 48).reshape(3, 4, 4)

print("iii.")
print(array)
print()

# ============================================================
# iv. Indexing and slicing
# ============================================================

# 1. 20.0
print("1.")
print(array[1, 0, 3])
print()

# 2. [9. 10. 11. 12.]
print("2.")
print(array[0, 2])
print()

# 3.
print("3.")
print(array[2])
print()

# 4.
print("4.")
print(array[:, 1, :2])
print()

# 5.
print("5.")
print(array[2, :, ::-1][:, :2])
print()

# 6.
print("6.")
print(array[:, :, 0][:, ::-1])
print()

# 7.
print("7.")
print(array[:, ::3, ::3].reshape(2, 2))
print()

# 8.
print("8.")
print(array[1, 2::-1][::-1])
print()