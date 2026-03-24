import statistics

floats = []
for i in range(10):
    floats.append(float(input("Enter a float: ")))

print("Sum: " + str(sum(floats)))
print("Max Index: " + str(floats.index(max(floats))))
print("Min Index: " + str(floats.index(min(floats))))
print("Mean: " + str(round(statistics.mean(floats), 2)))
print("Median: " + str(statistics.median(floats)))
