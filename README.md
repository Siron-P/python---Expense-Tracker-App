# python---Expense-Tracker-App
A personal expense tracker built in Python as a beginner project that helps you manage, categorize, and analyze your daily expenses - with csv export.

## Features

  - Add expenses with date, category, description and amount
  - View all expenses with total in a formatted table
  - Expenses Breakdown by category
  - Monthly overview grouped by month
  - Auto-save and load expenses from CSV file
  - CSV file for Monthly Summary

### Menu Options

1. Add Expense
2. View All Expenses
3. Expense Breakdown
4. Monthly Overview
5. View Chart
6. Delete Expense
7. Exit

### Categories

1. Food
2. Transport
3. Entertainment
4. Bills
5. Shopping
6. Education
7. Other

## CSV Files

### expense.csv

___Stores all expense records:___

Category,Amount,Description,Date

Bills,20000.0,Tution fee,2026-05-21

Transport,2500.0,tour,2026-02-05


### monthly_summary.csv

___Stores all monthly summary:___

Month,Total Amount

2026-02,2790.0

2026-03,2700.0

## Built With
 
  - Python 3 - Core Language
  - OS Module - File Handling
  - DateTime - Date parsing and Formatting

## Future Improvements 

  - Deleting Specific Expense Records
  - Adding charts from matplotlib
  - Add GUI using TKinter
