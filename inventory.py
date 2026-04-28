from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        '''
        In this function, you must initialise the following attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = int(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        '''
        Add the code to return the cost of the shoe in this method.
        '''
        return self.cost

    def get_quantity(self):
        '''
        Add the code to return the quantity of the shoes.
        '''
        return self.quantity

    def __str__(self):
        pass
        '''
        Add a code to returns a string representation of a class.
        '''
        return (f"{self.product} ({self.code})\n"
                f"{self.country}\n"
                f"${self.cost} | Quantity: {self.quantity}")


# =============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file
    represents data to create one object of shoes. You must use the try-except
    in this function for error handling. Remember to skip the first line using
    your code.
    '''
    try:
        with open("inventory.txt", "r") as file:  # Open file as read-only
            next(file)
            # Read line by line and save object parameters
            for line in file:
                shoe = line.split(",")
                shoe_obj = Shoe(shoe[0], shoe[1], shoe[2],
                                shoe[3], shoe[4])
                shoe_list.append(shoe_obj)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # Ask for user input
    print("__________________________")
    print("\nCapture new product data\n")
    country = input("Enter country: ")
    print(f"Country saved as '{country}'")
    code = input("Enter code: ")
    print(f"Code saved as '{code}'")
    product = input("Enter product: ")
    print(f"Product saved as '{product}'")

    # Ask for user input for cost and quantity with error-handling
    while True:
        try:
            cost = int(input("Enter cost: "))
            print(f"Cost saved as '{cost}'")
            break
        except ValueError:
            print("Invalid input. Please enter a number"
                  " without any other characters.")
    while True:
        try:
            quantity = int(input("Enter quantity: "))
            print(f"Quantity saved as '{quantity}'")
            break
        except ValueError:
            print("Invalid input. Please enter a number"
                  " without any other characters.")

    # Save user inputs as a Shoe object
    shoe_obj = Shoe(country, code, product,
                    cost, quantity)
    shoe_list.append(shoe_obj)
    print("\n\n**********\n"
          "Shoe added successfully!"
          "\n**********")

    input("\nEnter any character to return to the main menu.\n")


def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''
    print("__________________________")
    print("\nView all product data\n")
    # Save and print shoe_list as a table
    table = []
    for shoe in shoe_list:
        shoe_arr = [
            shoe.product,
            shoe.code,
            shoe.country,
            shoe.cost,
            shoe.quantity
        ]
        table.append(shoe_arr)
    headers = ["Product", "Code", "Country", "Cost ($)", "Quantity"]
    print(tabulate(table, headers=headers))

    input("\nEnter any character to return to the main menu.\n")


def update_inventory(updated_shoe):
    '''
    This helper function will update the new quantity in inventory.txt 
    based on the current value in shoe_list[].
    '''
    try:
        with open("inventory.txt", "r") as file:  # Open file as read
            lines = file.readlines()

        with open("inventory.txt", "w") as file:  # Open file as write
            file.write(lines[0])  # Write header line
            # Read line by line until matching code is found
            for line in lines[1:]:
                shoe = line.split(",")
                if shoe[1] == updated_shoe.code:
                    # Update the line with new quantity
                    line = (f"{shoe[0]},{shoe[1]},{shoe[2]},"
                            f"{shoe[3]},{updated_shoe.quantity}\n")
                file.write(line)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    print("__________________________")
    print("\nRestock product with lowest quantity\n")
    lowest_quantity_idx = 0
    # Find the lowest quantity shoe's index and print shoe
    for index, shoe in enumerate(shoe_list):
        if shoe.quantity < shoe_list[lowest_quantity_idx].quantity:
            lowest_quantity_idx = index
    print("********************************")
    print("Shoe with the lowest quantity:\n")
    print(shoe_list[lowest_quantity_idx])
    print("********************************")

    # Ask user to add quantity of shoes
    while True:
        answer = input("\nWould you like to add quantity of shoes? "
                       "(type 'y' or 'n') \n").lower().strip()
        if answer in ['y', 'yes']:
            # Ask user for quantity to add with error-handling
            while True:
                try:
                    new_quantity = int(input("Enter quantity to add: "))
                    shoe_list[lowest_quantity_idx].quantity += new_quantity
                    update_inventory(shoe_list[lowest_quantity_idx])
                    print("\nAdded successfully!")
                    print(f"\nQuantity added: '{new_quantity}'")
                    print("New quantity: "
                          f"{shoe_list[lowest_quantity_idx].quantity}")
                    break
                except ValueError:
                    print("Invalid input. Please enter a number.")
            input("\nEnter any character to return to the main menu.\n")
            return

        elif answer in ['n', 'no']:
            print("Quantity unchanged.")
            input("\nEnter any character to return to the main menu.\n")
            return


def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    print("__________________________")
    print("\nSearch product using code\n")
    # Ask user input for code to be searched
    while True:
        shoe_code = input("Please enter the shoe code: ")

        # If shoe is found, print and return
        for shoe in shoe_list:
            if shoe.code == shoe_code:
                print("\n\nShoe found!\n")
                print("********************************")
                print(shoe)
                print("********************************")

                input("\nEnter any character to return to the main menu.\n")
                return shoe

        # If shoe is not found, ask user if they want to try again
        while True:
            answer = input("Shoe not found. Try another code?"
                           "(type 'y' or 'n') ").lower().strip()
            if answer in ['y', 'yes']:
                break
            elif answer in ['n', 'no']:
                return None


def value_per_item():
    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''
    print("__________________________")
    print("\nView values of all products\n")
    # Create table with product and value (cost * quantity)
    table = []
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        table.append([shoe.product, value])

    # Print table
    headers = ["Product", "Value ($)"]
    print(tabulate(table, headers=headers))
    input("\nEnter any character to return to the main menu.\n")


def highest_qty():
    '''
    Write code to determine the product with the highest quantity and
    print this shoe as being for sale.
    '''
    print("__________________________")
    print("\nView product with the highest quantity\n")
    # Use linear search to find the highest quantity and its index
    highest = 0
    highest_idx = 0
    for index, shoe in enumerate(shoe_list):
        if shoe.quantity > highest:
            highest = shoe.quantity
            highest_idx = index

    # Print the shoe with the highest quantity
    print("********************************")
    print("Shoe with the highest quantity for sale:\n")
    print(shoe_list[highest_idx])
    print("********************************")

    input("\nEnter any character to return to the main menu.\n")


# ==========Main Menu=============
'''
Create a menu that executes each function above.
This menu should be inside the while loop. Be creative!
'''
read_shoes_data()
while True:
    print("__________________________")
    print("\nNike Warehouse Inventory Program\n")
    print("MAIN MENU")
    print("(1) Capture new product data\n"
          "(2) View all product data\n"
          "(3) Restock product with lowest quantity\n"
          "(4) Search product using code\n"
          "(5) View values of all products\n"
          "(6) View product with the highest quantity"
          "\n\nor q to quit")
    print("__________________________\n\n")

    user_input = input("Please select an option. \n")
    print(f"You entered: ({user_input})\n\n")
    if user_input == "1":
        capture_shoes()
    elif user_input == "2":
        view_all()
    elif user_input == "3":
        re_stock()
    elif user_input == "4":
        search_shoe()
    elif user_input == "5":
        value_per_item()
    elif user_input == "6":
        highest_qty()
    elif user_input == "q":
        print("\nThank you for using the Nike Warehouse Inventory Program."
              " Goodbye!\n")
        break
    else:
        print("\nPlease enter a valid option.\n")
