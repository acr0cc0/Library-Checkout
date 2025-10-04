## Author: Anthony Crocco 2025
## A GUI implementation of a library checkout app for Kolbe Cathedral
## Currently keeps track of loaned chromebooks 
## Future implementations will include support for library books and other materials
## and connecting to google sheets api

import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Configuration
FILE_NAME = 'loaners.xlsx'
WINDOW_TITLE = 'Library Checkout'

class LoanApp:

    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        
        self.df = self.load_data()

        self.fname_var = tk.StringVar()
        self.lname_var = tk.StringVar()
        self.num_var = tk.StringVar()
        self.date_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to add a new entry.")

        self.setup_ui()

    def load_data(self):
        try:
            # Try to read from the excel file
            df = pd.read_excel(FILE_NAME, index_col=0)
            print(f"Loaded {len(df)} records from {FILE_NAME}")
        except FileNotFoundError:
            # If the file doesn't exist, create a fresh DataFrame with the required columns
            df = pd.DataFrame(columns=['first-name', 'last-name', 'barcode-number', 'date'])
            print(f"'{FILE_NAME}' not found. Creating a new DataFrame.")
        except Exception as e:
            # Handle other potential read errors (e.g., file corrupted)
            messagebox.showerror("File Error", f"Error loading Excel file: {e}. Starting with an empty dataset.")
            df = pd.DataFrame(columns=['first-name', 'last-name', 'barcode-number', 'date'])
        return df

    def save_data(self):
        try:
            self.df.to_excel(FILE_NAME, engine='openpyxl')
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data to {FILE_NAME}: {e}")
            return False
        return True

    def setup_ui(self):
        pad_args = {'padx': 10, 'pady': 5}

        # Input Fields and Labels
        labels = [
            ("First Name:", self.fname_var), 
            ("Last Name:", self.lname_var), 
            ("Barcode Number:", self.num_var), 
            ("Date (mm-dd-yyyy):", self.date_var)
        ]

        for i, (text, var) in enumerate(labels):
            # Label
            lbl = tk.Label(self.master, text=text, font=('Arial', 10, 'bold'))
            lbl.grid(row=i, column=0, sticky='w', **pad_args)
            
            # Entry field
            entry = tk.Entry(self.master, textvariable=var, width=40, font=('Arial', 10))
            entry.grid(row=i, column=1, sticky='ew', **pad_args)
        
        # Add Entry Button 
        self.add_button = tk.Button(
            self.master, 
            text="Add Entry and Save to Excel", 
            command=self.add_entry,
            bg='white', 
            fg='black',    
            font=('Arial', 12, 'bold'),
            activebackground='#45A049',
            relief=tk.RAISED
        )
        self.add_button.grid(row=len(labels), column=0, columnspan=2, pady=15, padx=10, sticky='ew')

        # Status Bar 
        self.status_label = tk.Label(
            self.master, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor='w', # Align text to the west (left)
            font=('Arial', 9)
        )
        # Place the status bar at the bottom of the window
        self.status_label.grid(row=len(labels) + 1, column=0, columnspan=2, sticky='ew')

        # Configure grid to expand cleanly
        self.master.grid_columnconfigure(1, weight=1)

    def add_entry(self):        
        # Get and clean data from input variables
        fname = self.fname_var.get().strip()
        lname = self.lname_var.get().strip()
        num_str = self.num_var.get().strip()
        date = self.date_var.get().strip()
        
        # Validation
        if not all([fname, lname, num_str, date]):
            self.status_var.set("Error: All fields must be filled out.")
            return

        try:
            # Barcode number must be an integer
            barcode_num = int(num_str)
        except ValueError:
            self.status_var.set("Error: Barcode Number must be a whole number.")
            return

        # 3. Create the new row dictionary
        new_row = {
            'first-name': fname, 
            'last-name': lname, 
            'barcode-number': barcode_num, 
            'date': date
        }

        # Append to the DataFrame
        self.df = pd.concat([self.df, pd.Series(new_row).to_frame().T], ignore_index=True)

        # Save the updated DataFrame to Excel
        if self.save_data():
            self.status_var.set(f"SUCCESS: Added entry for {fname} {lname} and saved to {FILE_NAME}.")
            
            # Clear input fields after successful save
            self.fname_var.set("")
            self.lname_var.set("")
            self.num_var.set("")
            self.date_var.set("")
        else:
            self.status_var.set("FATAL ERROR: Could not save data. Check console for details.")


if __name__ == '__main__':
    # Initialize the root window
    root = tk.Tk()
    
    # Initialize the application class
    app = LoanApp(root)

    # Start the event loop
    root.mainloop()
