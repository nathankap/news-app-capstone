menu = ["coffee", "tea", "sandwich", "cake"]
stock = {"coffee": 10,
         "tea": 20,
         "sandwich": 5,
         "cake": 2}
price = {"coffee": 3.00,
         "tea": 2.50,
         "sandwich": 5.00,
         "cake": 4.00}

total_stock = 0.00
for item in menu:
    total_stock += stock[item] * price[item]

print(f"The total value of the stock is: ${total_stock:.2f}")