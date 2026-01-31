# Practical task M03T09

# import tabulate from the tabulate module to create table later
from tabulate import tabulate

#========The beginning of the class==========
class Shoe:
    # Constructor method
    def __init__(self, country, code, product, cost, quantity):
        '''
        Attributes:
            ● country,
            ● code,
            ● product,
            ● cost, and
            ● quantity.
        '''
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Method to return the cost of object
    def get_cost(self):
        '''
        Return the cost of the shoe in this method.
        '''
        return self.cost
    
    # Method to return the quantity of object
    def get_quantity(self):
        '''
        Return the quantity of the shoes.
        '''
        return self.quantity

    def __str__(self):
        '''
        Returns a string representation of a class.
        '''
        return (
            f"{self.country},{self.code},{self.product},"
            f"{self.cost},{self.quantity}"
            )


#=============Shoe list===========

# Initialize a shoe list
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():
    '''
    This function opens the file inventory.txt and read the data.
    It then creates a shoes object and appends it to the shoes list. 

    Return:
    The global shoe list
    '''
    shoe_list.clear() # write new current information to list
    
    try: # Open txt file in read mode
        with open("inventory.txt", "r") as file:
            # read the lines in split the into a list of substrings
            lines = file.read().split("\n")
            # clean each line
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            # Identify the headers and plit into substrings
            inventory_headers = cleaned_lines[0]
            header_line = inventory_headers.split(",") 
            # clean section of every line incase there are extra spaces       
            for line in cleaned_lines[1:]:
                part = line.split(",")
                country = part[0].strip()
                code = part[1].strip()
                product = part[2].strip()
                cost = float(part[3].strip())
                quantity = int(part[4].strip())
                # create a shoe onject and append to shoe_list
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
            return shoe_list
    # Error if file does not exist    
    except FileNotFoundError:
        print("File 'inventory.txt' does not exist.")

def update_file():
    '''
    This function will rewrite the file when data has
    changed oor been added.
    '''
    # create header string to be added to top of file
    headers = "Country,Code,Product,Cost,Quantity"
    try:
        with open("inventory.txt", "w") as file:
            file.write(headers + "\n") #add headers first
            for shoe in shoe_list:
                file.write(str(shoe) + "\n") # write in every shoe
        print("Inventory file was successfully updated with new informaiton")
    except Exception as e: # error message
        print(f"Something unexpected went wrong: {e}")


def capture_shoes():
    '''
    This function allows a user to capture data about a shoe.
    It then creates a shoe object and appends it to the shoe list.
    '''
    read_shoes_data() # read in current data

    # Request user input for the new shoe
    # .title() to capitilise the first characters
    # .upper() toe make any input uppercase
    # str() toe make sure the country is a str
    # float() to convert cost decimal values
    # int() to convert quantity to integer

    print("Follow the prompts to add a shoe to the Nike shoe inventory")
    product = input("What is the product name: ").title()
    while True:
        orig = input("What country did it originate from?: ").strip()
        # makes sure that the country is only alphabetical string
        if orig.replace(" ", "").replace("-", "").isalpha():
            country = orig.title()
            break
        else: # error if any numbers or symbols are entered
            print("Invalid input. Please try again.")
    code = input("What is the product's unique code: ").upper()
    while True:
        try:
            # makes sure cost is float
            cost = float(input("What is the cost of the product: R"))
            break
        except ValueError: # error if letters are entered
            print("Invalid input. Please enter mumerical values for cost.")
    while True:
        try:
            # makes sure quantity in integer
            quantity = int(input("What quantity do you wish to add: "))
            break
        except ValueError: # error if letters are entered
            print("Invalid input. Please enter numerical value for quantity.")
    # create an object witht the new details and append to shoe list
    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    print("Thank you for adding the new shoe.")

    # update the text file with new information
    update_file()

def view_all():
    '''
    This function iterates over the shoes list.
    It then print the details of each shoe in table format.

    Return:
    Details of each shoe in table.
    '''
    read_shoes_data() # read in freash data

    # make sure shoe list is not empty
    if len(shoe_list) == 0:
        print("There are no shoes to view")

    # create an empty list to make a table and append each attribute
    table = []
    for shoe in shoe_list:
        table.append([
            shoe.country,
            shoe.code,
            shoe.product,
            shoe.cost,
            shoe.quantity
    ])

    # set the headers for the table   
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print("This table contains all details for each shoe:")

    # create the table
    print(tabulate(table, headers = headers, tablefmt="grid"))

def re_stock():
    '''
    This function finds the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. 
    It then asks the user if they want to add this quantity of shoes.
    It then adds the quantity and updates it on the file for the shoe.
    '''
    read_shoes_data() # read in file data

    # sort list in ascending order according to the quantity
    shoe_list.sort(key = lambda shoe: shoe.get_quantity())
    low_shoe = shoe_list[0] # first line will be smalles quantity
    # print details and ask user if they want to add this quantity
    print(f'''
{low_shoe.product} (code: {low_shoe.code}) is \
low in stock with only {low_shoe.quantity} left.
Do you want to restock this shoe with {low_shoe.quantity} more?
''')
    
    # request user input to above question
    # .upper() to make any input uppercase
    choice = input("Y - Yes. N - No. Please enter your choice: ").upper()
    if choice == "Y":
        headers = "Country,Code,Product,Cost,Quantity"
        # double the quantity
        low_shoe.quantity = low_shoe.quantity * 2
        # write new details to file with update statement
        with open ("inventory.txt", "w") as file:
            file.write(headers + "\n")
            for shoe in shoe_list:
                file.write(str(shoe) + "\n")
        print(f"{shoe.product} has succsesfully been restocked.")
        # update file with new information
        update_file()
    elif choice == "N": # bye
        print("Thank you for checking up on low stock.")
    else: # Error in invalid input was entered
        print("Invalid option. Please try again")

def search_shoe():
    '''
    This function will search for a shoe from the list
    using the shoe code and return this object so that it will be printed.

    Return:
    The object of the shoe that was searched
    '''
    read_shoes_data() # read in file data

    # make sure shoe list is not empty
    if len(shoe_list) == 0:
        print("There are no shoes to view")

    # request user input for requested code and make it uppercase
    wanted_code = input("Please enter the code of the shoe: ").upper()
    for shoe in shoe_list:
        if shoe.code == wanted_code:
            return shoe # return the shoe details if shoe was fond
    else: # error for in no such shoe exist
        return "There is no shoe with that code. Please try again: "
    

def value_per_item():
    '''
    This function calculates and prints the total value for each item.

    Return:
    The total value of all shoes
    '''
    read_shoes_data() # read in file data
    
    # make sure shoe list is not empty
    if len(shoe_list) == 0:
        print("There are no shoes to view")
     
    print("Here are the total values for each shoe:")
    for shoe in shoe_list:
        # use methods to get cost and quantity for each shoe
        cost = shoe.get_cost()
        quantity = shoe.get_quantity()
        # calculate total value and print out for each shoe
        value = cost * quantity
        print(f"{shoe.product}: R{value}")


def highest_qty():
    '''
    This function determines the product with the highest quantity.
    It then prints this shoe as being for sale.

    Return:
    Shoe with highest quantity being on sale.
    '''
    read_shoes_data() # read in file data

    # make sure shoe list is not empty
    if len(shoe_list) == 0:
        print("There are no shoes to view")

    # sort the list in descending order according to quantity
    shoe_list.sort(key = lambda shoe: shoe.get_quantity(), reverse = True)
    shoe = shoe_list[0] # first shoe will have highest quantity
    print(f"{shoe.product} (code: {shoe.code}) is on sale for 40% off!")


#==========Main Menu=============

while True:
    print("Welcome to the menu of the Nike inventory stock list")
    # request user input for on of the options in menu
    menu = input(
        '''Please select one of the following options:
        cs - Capture a shoe you would like to add
        va - View all shoes
        rs - Restock the shoe with the lowest quantity
        ss - Search for a specific shoe using its unique code
        vpi - See what the total value for each shoe is
        hq - See which shoe is for sale (shoe with highest quantity)
        ex - Exist the menu
        '''
    ).lower() # make any input lowercase
    
    # execute functions according to user input 
    if menu == "cs":
        capture_shoes()
    elif menu == "va":
        view_all()
    elif menu == "rs":
        re_stock()
    elif menu == "ss":
        print(search_shoe())
    elif menu == "vpi":
        value_per_item()
    elif menu == "hq":
        highest_qty()
    elif menu == "ex":
        print("Thank you for checking.Bye")
        break # exit function by breaking out loop
    else: # error if anything else is entered
        print("Invalid choice. Please choose again.")