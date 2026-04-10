def sum_recursion(list_int, index):
    total = 0
    size = len(list_int)

    if index == 0:
        total = list_int[index]
    elif 0 < index < size:
        total = list_int[index] + sum_recursion(list_int, index - 1)
    else:
        print("Invalid index.")

    return total


print(sum_recursion([4, 3, 1, 5], 1))
