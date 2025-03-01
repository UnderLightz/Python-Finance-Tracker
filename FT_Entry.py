from datetime import datetime

date_format = "%m-%d-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime(date_format)
    #"f" in strftime is for formatting
    #"%d-%m-%Y" is the format of the date (day-month-year)

    try:
        valid_date = datetime.strptime(date_str, date_format)
        #tries to convert the date string into a datetime object
        #"p" in strptime is for parsing
        #parsing typically involves converting a string into a more structured format that a program can work with
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date format. Please use MM-DD-YYYY")
        return get_date(prompt, allow_default)
#this is a recursive function, it will keep prompting the user for a valid date

def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        return amount
    except ValueError as e:
        #e is the error message
        print(e)
        return get_amount()

def get_category():
    category = input("Enter the category: ('I' for Income or 'E' for Expense)").upper()
    if category in CATEGORIES:
        return category
    
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense")
    return get_category()


def get_description():
    return input("Enter the description (optional): ")