## Author: Anthony Crocco 2025
## A GUI implementation of a library checkout app for my school
## Currently keeps track of loaned chromebooks 
## Future implementations will include support for library books and other materials
import tkinter as tk
from tkinter import messagebox
import gspread
from google.oauth2.service_account import Credentials
from tkcalendar import DateEntry 

# --- Configuration ---
SHEET_NAME = 'test'
SERVICE_ACCOUNT_FILE = 'credentials.json'

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

class LoanApp:
    def __init__(self, master):
        self.master = master
        master.title("Google Sheets Loaner Entry")
        
        # Tkinter variables
        self.fname_var = tk.StringVar()
        self.lname_var = tk.StringVar()
        self.num_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        # Connect immediately
        self.sheet = None
        self.connect_to_sheets()

        # Build the UI
        self.setup_ui()

    def connect_to_sheets(self):
        self.status_var.set("Connecting to Google Sheets...")
        try:
            creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            client = gspread.authorize(creds)
            
            # attempting to open
            self.sheet = client.open(SHEET_NAME).sheet1
            
            self.status_var.set(f"Connected to '{SHEET_NAME}'. Ready.")
            print("Connection Successful")
        except Exception as e:
            self.status_var.set(f"Error: {e}")
            messagebox.showerror("Connection Error", f"Could not connect.\nError: {e}")

    def setup_ui(self):
        input_frame = tk.Frame(self.master, padx=10, pady=10)
        input_frame.pack(fill='x')

        # --- Standard Text Inputs ---
        labels = [
            ("First Name:", self.fname_var, 0), 
            ("Last Name:", self.lname_var, 1), 
            ("Barcode Number:", self.num_var, 2)
        ]

        for text, var, row in labels:
            tk.Label(input_frame, text=text, font=('Arial', 10, 'bold')).grid(row=row, column=0, sticky='w', pady=5)
            tk.Entry(input_frame, textvariable=var, width=30).grid(row=row, column=1, pady=5)

        # --- Date Picker Widget ---
        tk.Label(input_frame, text="Date:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=5)
        
        self.date_entry = DateEntry(input_frame, width=27, background='darkblue',
                                    foreground='white', borderwidth=2, date_pattern='mm/dd/yyyy')
        self.date_entry.grid(row=3, column=1, pady=5)

        # --- Submit Button ---
        btn = tk.Button(self.master, text="Add Entry", command=self.add_entry, 
                        bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'))
        btn.pack(pady=10, ipadx=20)

        # --- Status Bar ---
        status_label = tk.Label(self.master, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor='w')
        status_label.pack(side='bottom', fill='x')

    def add_entry(self):
        fname = self.fname_var.get()
        lname = self.lname_var.get()
        num_str = self.num_var.get()
        date_str = self.date_entry.get()

        if not all([fname, lname, num_str, date_str]):
            messagebox.showwarning("Missing Data", "Please fill in all fields.")
            return

        try:
            num = int(num_str)
        except ValueError:
            messagebox.showerror("Invalid Input", "Barcode must be a number.")
            return

        try:
            new_row = [fname, lname, num, date_str]
            self.sheet.append_row(new_row)
            
            self.status_var.set(f"Added: {fname} {lname} on {date_str}")
            
            self.fname_var.set("")
            self.lname_var.set("")
            self.num_var.set("")
            # Set focus back to first name
            self.master.children[list(self.master.children.keys())[0]].children['!entry'].focus_set()
            
        except Exception as e:
            messagebox.showerror("API Error", f"Failed to save data: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = LoanApp(root)
    root.mainloop()
