# Function to sort array using insertion sort
def insertionSort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


# A utility function to print array of size n
def printArray(arr):
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


def binary_search(target, items):
    low, high = 0, len(items) - 1

    # Keep iterating until the low and high cross
    while high >= low:
        # Find midpoint
        mid = (low + high) // 2

        # If item is found at midpoint, return its index
        if items[mid] == target:
            return mid
        # Else, if item at midpoint is less than target,
        # search the second half of the list
        elif items[mid] < target:
            low = mid + 1
        # Else, search the first half
        else:
            high = mid - 1

    # Returns None if item not found
    return None


def interpolation_search(data, arr):
    lo = 0
    hi = len(arr) - 1
    mid = -1
    comparisons = 1
    index = -1
    while (lo <= hi):
        # print("Comparison ", comparisons)
        # print("lo : ", lo)
        # print("list[", lo, "] = ")
        # print(arr[lo])
        # print("hi : ", hi)
        # print("list[", hi, "] = ")
        # print(arr[hi])
        comparisons = comparisons + 1

        # probe the mid point
        mid = lo + (((hi - lo) * (data - arr[lo])) // (arr[hi] - arr[lo]))
        # print("mid = ", mid)

        # data found
        if (arr[mid] == data):
            index = mid
            break
        else:
            if (arr[mid] < data):
                # if data is larger, data is in upper half
                lo = mid + 1
            else:

                # if data is smaller, data is in lower half
                hi = mid - 1
    # print("Total comparisons made: ")
    # print(comparisons-1)
    return index


arr = [27, -3, 4, 5, 35, 2, 1, -40, 7, 18, 9, -1, 16, 100]
location = interpolation_search(9, arr)

print("Element found at location: ", (location))

# TASK ANSWERS
# Binary search is a good choice for this specific list because
# the number being searched for (9) is near the midpoint of the
# sorted list. It will take less time to search for this number
# with binary search.

# Interpolation Search is better than binary search when values
# are sorted in a uniformly distributed way. Binary search always
# goes to the middle, but interpolation search can go to different
# locations.
