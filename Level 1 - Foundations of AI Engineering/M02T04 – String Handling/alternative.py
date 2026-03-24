input = input("Please input a string: ")
input_list = list(input)
j = 0
for i in input_list:
    j += 1
    if j % 2 == 0:
        input_list[j-1] = i.upper()
    else:
        input_list[j-1] = i.lower()

input_str = "".join(input_list)
print("Alternating characters: " + input_str)

input_str = input_str.lower().split()

input_list = list(input_str)
j = 0
for i in input_list:
    j += 1
    if j % 2 == 0:
        input_list[j-1] = i.upper()
    else:
        input_list[j-1] = i.lower()

print("Alternating words: " + " ".join(input_list))
