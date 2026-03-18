swim = int(input("How many minutes for swimming? "))
cycle = int(input("How many minutes for cycling? "))
run = int(input("How many minutes for running? "))

total_minutes = swim + cycle + run
print(f"Total time taken for the triathlon: {total_minutes} minutes")

if total_minutes < 100:
    print("Award: Provincial colours")
elif total_minutes < 105:
    print("Award: Provincial half colours")
elif total_minutes < 110:
    print("Award: Provincial scroll")
else:
    print("No award.")