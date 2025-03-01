import pandas as pd
import csv
from datetime import datetime
from FT_Entry import get_date, get_amount, get_category, get_description
#pulls data inout from the FT_Entry file
import matplotlib.pyplot as plt
#used for plotting data on a graph

class CSV:
    CSV_FILE = "FinanceTracker.csv"
    #class is a blueprint for creating objects
    #in this case, class creates a CSV object
    COLUMNS = ["Date", "Amount", "Category", "Description"]
    FORMAT = "%m-%d-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            #data frame is an object within pandas to access different rows and columns
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "Date": date,
            "Amount": amount,
            "Category": category,
            "Description": description
        }
        #this is a python dictionary
        #allows data to be written into the correct columns
        with open(cls.CSV_FILE, mode="a", newline="") as csvfile:
        #"a" is append mode, which allows data to be added to the end of the file
        #this line automatically closes the file after the block of code is executed
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            #takes dictionary and write into the csv file
            writer.writerow(new_entry)
        print("Entry added successfully")
    #this function is used to add a new entry to the csv file

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["Date"] = pd.to_datetime(df["Date"], format=CSV.FORMAT)
        #converts the date column to a datetime object
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)
        #converts the start and end date to datetime objects

        mask = (df["Date"] >= start_date) & (df["Date"] <= end_date)
        #checks if the data in the front row is greater than the start date and less than the end date
        #compares the dates since date in datetime format
        filtered_df = df.loc[mask]
        #filters the data based on the mask

        if filtered_df.empty:
            print("No transactions found in the date range")
        else:
            print(f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"Date": lambda x: x.strftime(CSV.FORMAT)}
                #"x" is the date column and gets formatted to the date format
                )
            )

            total_income = filtered_df[filtered_df["Category"] == "Income"]["Amount"].sum()
            total_expense = filtered_df[filtered_df["Category"] == "Expense"]["Amount"].sum()
            #sums up all the income and expense transactions
            print("\nSummary:")
            print(f"Total Income: {total_income:.2f}")
            #".2f" is used to round to the nearst 2 decimal places
            print(f"Total Expense: {total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df    
    #gives all the transactions in a date range


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (MM-DD-YYYY) or enter for today's date: ", allow_default=True)
    #allow default is set to true, so if the user doesn't enter a date, it will default to today's date
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    df.set_index("Date", inplace=True)

    income_df = (
        df[df["Category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
    )
    #"D" is for daily frequency
    #resample is used to change the frequency of the data
    #reindex(df.index,fill_value=0) is used to fill in the missing dates with 0

    expense_df = (
        df[df["Category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index,fill_value=0)
    )

    plt.figure(figsize=(10, 6))
    #sets the size of the graph
    plt.plot(income_df.index, income_df["Amount"], label="Income", color="green")
    #plots the income data on the graph in green
    plt.plot(expense_df.index, expense_df["Amount"], label="Expense", color="red")
    #plots the expense data on the graph in red
    plt.xlabel("Date")
    #sets the x-axis label as the date
    plt.ylabel("Amount")
    #sets the y-axis label as the amount
    plt.title("Income vs Expense")
    #givces the graph a title
    plt.legend()
    #adds a legend to the graph
    plt.grid()
    #adds a grid to the graph
    plt.show()
    #shows the graph


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (MM-DD-YYYY): ")
            end_date = get_date("Enter the end date (MM-DD-YYYY): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to plot the transactions? (y/n): ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
#this is the main function that runs the program
#it will keep running until the user decides to exit
#"if __name__ == "__main__":" is used to check if the script is being run directly or being imported
#protects the code from being run when imported