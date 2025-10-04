## Author: Anthony Crocco 2025
## A CLI program to track loaner chromebooks for Kolbe Cathedral
## This is a basic precursor to the final version which will be a GUI implementation
## ant connected to google sheets via API to streamline access
## Imports an excel file, turns the contents into a dataframe, appends new
## loaner information to the dataframe and exports back to the same excel file

import pandas as pd

file = 'loaners.xlsx'
list = pd.read_excel(file, index_col='index')
df = pd.DataFrame(list)
x = True
while x:

    fname = str(input('Enter first name: '))
    lname = str(input('Enter last name: '))
    num = int(input('Enter barcode number: '))
    date = str(input('Enter date (mm-dd-yyyy): '))

    new_row = {'first-name': fname, 'last-name': lname, 'barcode-number':num, 'date': date}
    df = df._append(new_row, ignore_index=True)
    df.to_excel('loaners.xlsx', engine='openpyxl')
    cont = str(input('Add another? (y/n): '))
    if cont =='n':
        x = False
        break

