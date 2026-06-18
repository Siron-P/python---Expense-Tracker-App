import os
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class Expense:
    def __init__(self):
        self.categories = ["Food","Transport","Entertainment","Bills","Shopping","Education","Others"]
        self.conn = sqlite3.connect("Expenses.db")
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.create_table()
        self.load_expense()

    def display_heading(self):
        print(f"{'='*37}\n|{' '*9} EXPENSE TRACKER {' '*9}|\n{'='*37}\n")

    def display_menu(self):
        print("1. Add Expense")
        print("2. View All Expense")
        print("3. View Expense Breakdown")
        print("4. Monthly Overview")
        print("5. View Chart")
        print("6. Delete Expense")
        print("7. Exit the program....")
        print("_"*37,"\n")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id          INTEGER PRIMARY KEY  AUTOINCREMENT,
                date        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                description TEXT,
                amount      REAL    NOT NULL
            )
        """)

    def load_expense(self):
        self.cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        rows = self.cursor.fetchall()
        self.expenses = [dict(row) for row in rows]
        print(f"Loaded {len(self.expenses)} expenses")

    def save_to_db(self,expense):
        self.cursor.execute(
            "INSERT INTO expenses (Category, Amount, Description, Date) VALUES (?,?,?,?)",
            (expense["Category"],expense["Amount"],expense["Description"],expense["Date"])
        )
        self.conn.commit()

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

        #calling save_to_db() and printing saved details
        self.save_to_db(expenses)

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
        
        self.display_heading()
        print("Expenses Breakdown")
        print(f"{'-'*37}")

        total_category = {}
        for expense in self.expenses:
            category = expense["Category"]
            total_category[category] = total_category.get(category,0)+expense["Amount"]

        print("\nCATEGORIES :\n")
        print("1. Food")
        print("2. Transport")
        print("3. Entertainment")
        print("4. Bills")
        print("5. Shopping")
        print("6. Education")
        print("7. Other")
        print("8. All")
        try:
            choose_exp = int(input("🔢 Choose any option for its expense (1/2/3/4/5/6/7/8) : "))

            all_category = {1:"Food",2:"Transport",3:"Entertainment",4:"Bills",5:"Shopping",6:"Education",7:"Others"}

            print("-"*65)

            if choose_exp == 8:
                for category, total in sorted(total_category.items()):
                    print(f"{category:<20}Rs.{total:.2f}")

            elif choose_exp in all_category:
                for id, expenses in enumerate(self.expenses,1):
                    if expenses['Category'] == all_category[choose_exp]:
                        print(f"{expenses['Date']:<12}{expenses['Category']:<19}{expenses['Description']:<20} Rs. {expenses['Amount']:<10}")

                user_choice = all_category[choose_exp]
                total = total_category.get(user_choice,0)
                if total == 0:
                    print(f"No expense found in this category : {all_category[choose_exp]} ")
                else:
                    print("="*66)
                    print(f"{user_choice:<20} Rs.{total:.2f}")
                    print("="*66)

            else:
                print("Please choose valid option.")
        except ValueError:
            print("Please enter a valid number!")

        input("\nPress 'Enter' to return to menu.\n")

    def monthly_overview(self):
        self.display_heading()
        print(f"MONTHLY OVERVIEW\n{'_'*37}")

        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return

        total_amt = {}
        for expense in self.expenses:
            date = expense["Date"]
            month = date[5:7]
            if month not in total_amt:
                total_amt[month] =  {"dates":[],"total":0}
            total_amt[month]["dates"].append(date)
            total_amt[month]["total"]+= expense["Amount"]

        for month,data in sorted(total_amt.items()):
            print(f"\nMonth : {month}")
            print(f"{'Date':<15} {'Amount':>10}")
            print("-" * 25)
            for expense in self.expenses:
                if expense["Date"][5:7] == month:
                    print(f"{expense['Date']:<15} Rs.{expense['Amount']:>8.2f}")
            print("-" * 25)
            print(f"{'Total':<15} Rs.{data['total']:>8.2f}")
        
        input("\nPress 'Enter' to return to menu\n")

    def bar_chart(self):
        
        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return
        
        total_category = {}
        for expense in self.expenses:
            category = expense["Category"]
            total_category[category] = total_category.get(category,0)+expense["Amount"]

        x_category = list(total_category.keys())
        y_category = list(total_category.values())

        plt.bar(x_category,y_category,color='black',linewidth= 0.8)
        plt.title('Expenses Bar Chart',fontsize=20,fontname='DejaVu Serif',fontweight='bold')
        plt.xlabel('Categories',fontsize=15,fontname='DejaVu Serif',fontweight='bold')
        plt.ylabel('Amount',fontsize=15,fontname='DejaVu Serif',fontweight='bold')
        plt.tight_layout()
        plt.show()

        input("\nPress 'Enter' to return to menu\n")

    def line_chart(self):
        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return
        
        total_category = {}
        for expense in self.expenses:
            category = expense["Category"]
            total_category[category] = total_category.get(category,0)+expense["Amount"]

        x_category = list(total_category.keys())
        y_category = list(total_category.values())

        plt.plot(x_category,y_category,marker="o",color='black')
        plt.title('Expenses Bar Chart',fontsize=20,fontname='DejaVu Serif',fontweight='bold')
        plt.xlabel('Categories',fontsize=15,fontname='DejaVu Serif',fontweight='bold')
        plt.ylabel('Amount',fontsize=15,fontname='DejaVu Serif',fontweight='bold')
        plt.tight_layout()
        plt.show()

        input("\nPress 'Enter' to return to menu\n")

    def pie_chart(self):
        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return
        
        total_category = {}
        for expense in self.expenses:
            category = expense["Category"]
            total_category[category] = total_category.get(category,0)+expense["Amount"]

        x_category = list(total_category.keys())
        y_category = list(total_category.values())

        plt.pie(y_category,labels=x_category, colors=['lightgreen','mediumseagreen','seagreen','teal','mediumaquamarine','darkgreen'])
        plt.title('Expenses Pie Chart',fontsize=20,fontname='DejaVu Serif',fontweight='bold')
        plt.tight_layout()
        plt.legend(title="Categories",loc='lower right',frameon=True,ncol=2,markerscale=1.5)
        plt.show()

        input("\nPress 'Enter' to return to menu\n")

    def delete(self):
        self.display_heading()
        print(f"Delete Expense\n{'_'*37}")
        
        if not self.expenses:
            print("\nNo Expenses Found!")
            print("Please add expenses from the option 1.")
            input("Press 'enter' to return to menu.\n")
            return
        
        print(f"\n{'ID:<5'} {"Category":<18} {"Amount":<9} {"Date":<12}")
        print("-"*65)
        for expense in self.expenses:
            print(f"{expense['ID']:<5} {expense['Category']:<18} {expense['Amount']:<9} {expense['Date']:<12}")

        try:
            delete_id = int(input("\nChoose ID no. which you would like to delete : "))
            print(f"ID : {delete_id}")
        except ValueError:
            print("Please enter a valid number!")
            input("\nPress 'Enter' to return to menu\n")
            return
        
        if delete_id<1 or delete_id>len(self.expenses):
            print("Please enter valid ID!")
            input("\nPress 'Enter' to return to menu\n")
            return
        
        confirm = input(f"Are you sure you want to delete {delete_id}? (Yes/No) : ")
        if confirm.lower == "yes":
            self.cursor.execute("DELETE FROM expenses WHERE id = ?",(delete_id))
            self.conn.commit()
            self.load_expense()
            print("-")*37
            print(f"Expenses Deleted!")
            print("-")*37
        else:
            print("Deletion cancelled.")
        
        input("\nPress 'Enter' to return to menu\n")

    def run_program(self):
        self.display_heading()

        while True:
            try:
                self.display_menu()
                choice = int(input("Choose any one option (1/2/3/4/5/6/7) : "))
                if choice == 1:
                    print("\n")
                    self.add_expense()
                elif choice == 2:
                    self.view_all_expense()
                elif choice == 3:
                    self.exp_breakdown()
                elif choice == 4:
                    self.monthly_overview()
                elif choice == 5:
                    self.display_heading()
                    print("Expenses Chart")
                    print(f"{'-'*37}")
                    print("Type of Charts : \n ")
                    print("1. Bar Chart ")
                    print("2. Line Chart")
                    print("3. Pie Chart\n")
                    chart_input = int(input("Choose any one option (1/2/3) : "))
                    if chart_input == 1:
                        self.bar_chart()
                    elif chart_input == 2:
                        self.line_chart()
                    elif chart_input == 3:
                        self.pie_chart()
                    else:
                        print("Please enter valid option!")
                elif choice == 6:
                    self.delete()
                elif choice == 7:
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