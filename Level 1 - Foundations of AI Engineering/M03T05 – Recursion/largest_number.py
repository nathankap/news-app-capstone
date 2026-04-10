def largest_number(list_int):
    if list_int:
        first = list_int.pop(0)
        if list_int:
            second = largest_number(list_int)
        else:
            return first

    return first if first > second else second


print(largest_number([1, 4, 5, 3]))
print(largest_number([3, 1, 6, 8, 2, 4, 5]))
