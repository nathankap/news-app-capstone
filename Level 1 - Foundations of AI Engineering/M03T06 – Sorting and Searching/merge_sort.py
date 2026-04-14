def merge_sort(items):
    # Get the length of the input list
    items_length = len(items)

    # Create temporary storage for merging
    temporary_storage = [None] * items_length

    # Initialise the size of subsections to 1
    size_of_subsections = 1

    # Iterate until the size of subsections is less than the length of the list
    while size_of_subsections < items_length:
        # Iterate over the list in steps of size_of_subsections * 2
        for i in range(0, items_length, size_of_subsections * 2):
            # Determine the start and end indices of the two subsections
            # to merge.
            first_section_start, first_section_end = i, min(
                i + size_of_subsections, items_length
            )
            second_section_start, second_section_end = first_section_end, min(
                first_section_end + size_of_subsections, items_length
            )
            # Define the sections to merge
            sections = (first_section_start, first_section_end), (
                second_section_start,
                second_section_end,
            )
            # Call the merge function to merge the subsections
            merge(items, sections, temporary_storage)

        # Double the size of subsections for the next iteration
        size_of_subsections *= 2
    # Return the sorted list
    return items


def merge(items, sections, temporary_storage):
    # Unpack the sections tuple to get the start and end indices
    # of each section.
    (first_section_start, first_section_end), (
        second_section_start,
        second_section_end,
    ) = sections
    # Initialise indices for the two sections and temporary storage
    left_index = first_section_start
    right_index = second_section_start
    temp_index = 0
    # Loop until both sections have been fully merged
    while left_index < first_section_end or right_index < second_section_end:
        # Check if both sections still have elements to compare
        if left_index < first_section_end and right_index < second_section_end:
            # Compare elements from both sections
            if len(items[left_index]) < len(items[right_index]):
                # Place the smaller element into temporary storage
                temporary_storage[temp_index] = items[left_index]
                left_index += 1
            else:  # items[right_index] <= items[left_index]
                temporary_storage[temp_index] = items[right_index]
                right_index += 1
            temp_index += 1

        # If section 1 still has elements left to merge
        elif left_index < first_section_end:
            # Copy remaining elements from section 1 to temporary storage
            for i in range(left_index, first_section_end):
                temporary_storage[temp_index] = items[left_index]
                left_index += 1
                temp_index += 1
        # If section 2 still has elements left to merge
        else:  # right_index < second_section_end
            # Copy remaining elements from section 2 to temporary storage
            for i in range(right_index, second_section_end):
                temporary_storage[temp_index] = items[right_index]
                right_index += 1
                temp_index += 1

    # Copy sorted elements from temporary storage back to the original list
    for i in range(temp_index):
        items[first_section_start + i] = temporary_storage[i]


first_list = ["abc", "d", "efgh", "ij", "klmnop", "qrs", "tuvwxyz", "now",
              "i", "know"]
print(f"first list: {first_list}")
second_list = ["12", "3", "456789", "101112", "1314151617181920212223242526",
               "2728", "2930", "3132", "i", "know"]
print(f"second list: {second_list}")
third_list = ["dawtsinsung", "is", "someone", "i", "love", "endlessly", "and",
              "ill", "continue", "lovingheruntiltheendoftime"]
print(f"third list: {third_list}\n\n")
sorted_list_1 = merge_sort(first_list)
sorted_list_2 = merge_sort(second_list)
sorted_list_3 = merge_sort(third_list)
print(sorted_list_1)
print(sorted_list_2)
print(sorted_list_3)
