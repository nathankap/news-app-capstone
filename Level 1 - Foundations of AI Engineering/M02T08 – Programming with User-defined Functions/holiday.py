def hotel_cost(num_nights):
    return num_nights * 140


def plane_cost(city_flight):
    if city_flight == "LAX":
        return 500
    elif city_flight == "IND":
        return 300
    elif city_flight == "ORD":
        return 400
    else:
        return 0


def car_rental(rental_days):
    return rental_days * 40


def holiday_cost(num_nights, city_flight, rental_days):
    total_cost = (hotel_cost(num_nights) + plane_cost(city_flight) +
                  car_rental(rental_days))
    return total_cost


city_flight = input("Enter the city you are flying to (LAX, IND, ORD): ")
num_nights = int(input("Enter the number of nights you will be staying: "))
rental_days = int(input("Enter the number of days you will be renting a car: "))

total = holiday_cost(num_nights, city_flight, rental_days)
print(f"The total cost of your holiday is: ${total}")
