import csv
import os
from datetime import datetime

class Expense:
    def __init__(self):
        self.expenses = []
        self.categories = ["Food","Transport","1tainment","Bills","Shopping","Education","Others"]
        self.file_name = "Expense.csv"
        self.load_expense()

    def display_heading(self):
        print(f"{'='*37}\n|{' '*9} EXPENSE TRACKER {' '*9}|\n{'='*37}\n")

    def display_menu(self):
        print("1. Add Expense")
        print("2. View All Expense")
        print("3. View Expense Breakdown")
        print("4. Monthly Overview")
        print("5. Delete Expense")
        print("6. Exit the program....")
        print("_"*37,"\n")

    def load_expense(self):
        if not os.path.exists(self.file_name):
            with open(self.file_name, "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["Category","Amount", "Description", "Date"])
            print(f"File not found! Created new file: {self.file_name}\n")
            return
        
        self.expenses.clear()
        with open(self.file_name,'r',newline="") as file:
                reader = csv.reader(file)
                next(reader, None) #header row will be skipped
                for row in reader: 
                        if row:  #Checking if row is empty or nott
                            self.expenses.append({
                                "Category": row[0],
                                "Amount": float(row[1]),
                                "Description": row[2],
                                "Date": row[3]
                            })
        print(f"File found! Loaded {len(self.expenses)} expenses from {self.file_name}\n")

    def save_to_csv(self, expense):
        with open(self.file_name,"a",newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                expense["Category"],
                expense["Amount"],
                expense["Description"],
                expense["Date"]
            ])

    def add_expense(self):
        self.display_heading()
        print(f"ADD NEW EXPENSE\n{'_'*37}")

        print("CATEGORIES :\n")
        print("1. Food")
        print("2. Transport")
        print("3. Entertainment")
        print("4. Bills")
        print("5. Shopping")
        print("6. Education")
        print("7. Other")

        #For choice of category 
        while True:
            try:
                cate_choice = int(input(" 🔢 Choose any option (1/2/3/4/5/6/7) : "))
                if 1 <= cate_choice <= len(self.categories) :
                    category = self.categories[cate_choice-1]
                    break
                else:
                    print("Invalid choice. Please select again!")
            except ValueError:
                print("Please enter a valid number!")

        #For Input of expense amount
        while True:
            try:
                amount = float(input("Enter the amount you spent : "))
                if amount > 0:
                    break
                else:
                    print("Amount must be a positive.")
            except ValueError:
                print("Please enter a valid amount!")

        #For the description of expense
        while True:
            description = input("Enter the description : ").strip()
            if not description:
                description = "No description"
            else:
                break

        #for the date
        while True:
            try:
                input_date = input("Enter date (YYYY-MM-DD) or press 'ENTER' for today's date : ").strip()
                
                if not input_date:
                    now = datetime.now()
                    date = now.strftime("%Y-%m-%d") #strftime = string format time (Convert datetime to string)
                    break
                else:
                    datetime.strptime(input_date,"%Y-%m-%d") #strptime = string parse time (Convert string to datetime)
                    date = input_date
                    break
            except ValueError:
                print("Invalid date format! Please enter in calid format.")

        #dictionary to store expenses details
        expenses = {
            "Category" : category,
            "Amount" : amount,
            "Description" : description,
            "Date" : date
        }

        #calling save_to_csv() and printing saved details
        self.save_to_csv(expenses)
        self.expenses.append(expenses)

        print(f'{"-"*37}')
        print("EXPENSE ADDED!")
        print("-"*37)
        print(f"\n {'Category :':<15} | {category:<20}")
        print(f"\n {'Amount :':<15} | Rs. {amount:<16}")
        print(f"\n {'Description :':<15} | {description:<20}")
        print(f"\n {'Date :':<15} | {date:<20}")
        print(f'{"-"*37}\n')
        
        input("Press 'Enter' to return to menu.")

    def view_all_expense(self):
        self.display_heading()
        print(f"VIEW ALL EXPENSES\n{'_'*37}")

        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return
        
        print(f"\nTotal Number of Expenses Entered = {len(self.expenses)}")

        print("-"*70)
        print(f"{'S.N':<4}{'Date':<12}{'Category':<15}{'Description':<20}{'Amount':<10}")
        print("-"*70)

        total_amt = 0
        for id, expenses in enumerate(self.expenses,1):
            print(f"{id:<4}{expenses['Date']:<12}{expenses['Category']:<15}{expenses['Description']:<20} Rs. {expenses['Amount']:<10}")
            total_amt += expenses['Amount']

        print("-"*70)
        print(f"{'Total Expense :':<50} Rs. {total_amt:<10}")
        print("-"*70)
        input("\nPress 'Enter' to return to menu page")

    def exp_breakdown(self):
        if not self.expenses:
            print("No Expenses Found!\n")
            return
        
        print(f"{'-'*37}")
        print("Expenses Breakdown")
        print(f"{'-'*37}")

        total_category = {}
        for expense in self.expenses:
            category = expense["Category"]
            total_category[category] = total_category.get(category,0)+expense["Amount"]

        print("CATEGORIES :\n")
        print("1. Food")
        print("2. Transport")
        print("3. Entertainment")
        print("4. Bills")
        print("5. Shopping")
        print("6. Education")
        print("7. Other")
        print("8. All")
        choose_exp = int(input("🔢 Choose any option for its expense (1/2/3/4/5/6/7/8) : "))

        all_category = {1:"Food",2:"Transport",3:"Entertainment",4:"Bills",5:"Shopping",6:"Education",7:"Other"}

        if choose_exp == 8:
            for category, total in sorted(total_category.items()):
                print("-"*70)
                print(f"{category:<20}Rs.{total:.2f}")
                print("-"*70)
                input("Press 'Enter' to return to menu.")

        elif choose_exp in all_category:
            print("-"*66)
            for id, expenses in enumerate(self.expenses,1):
                if expenses['Category'] == all_category[choose_exp]:
                    print(f"{expenses['Date']:<12}{expenses['Category']:<15}{expenses['Description']:<20} Rs. {expenses['Amount']:<10}")

            user_choice = all_category[choose_exp]
            total = total_category.get(user_choice,0)
            if total == 0:
                print(f"No expense found in this category : {all_category[choose_exp]} ")
            else:
                print("="*66)
                print(f"{user_choice:<20} Rs.{total:.2f}")
                print("="*66)
                input("Press 'Enter' to return to menu.\n")

        else:
            print("Please choose valid option.")


    def run_program(self):
        self.display_heading()

        while True:
            try:
                self.display_menu()
                choice = int(input("Choose any one option (1/2/3/4/5/6) : "))
                if choice == 1:
                    print("\n")
                    self.add_expense()
                elif choice == 2:
                    self.view_all_expense()
                elif choice == 3:
                    self.exp_breakdown()
                elif choice == 4:
                    print("code Left")
                elif choice == 5:
                    print("code Left")
                elif choice == 6:
                    print("\nExiting the program .....\n")
                    break
                else:
                    print("Invalid Choice. Please try again!!")
            except ValueError:
                print("Please enter a valid number!")
                input("\nPress on 'Enter' to continue the program....")

if __name__ == "__main__":
    expense_tracker = Expense()
    expense_tracker.run_program()