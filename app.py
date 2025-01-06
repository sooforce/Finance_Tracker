import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# File path for saving and loading expenses
file_path = 'expenses.csv'

# Initialize or load expense data
if os.path.exists(file_path):
    expenses = pd.read_csv(file_path)
else:
    expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# Function to save expenses to a CSV file
def save_expenses():
    expenses.to_csv(file_path, index=False)

# Function to add or update an expense
def add_or_update_expense(edit_index=None):
    date = date_entry.get()
    category = category_combobox.get()
    amount = amount_entry.get()
    description = description_entry.get()

    if not date or not category or not amount:
        messagebox.showwarning("Input Error", "Please fill in all required fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid amount.")
        return

    new_expense = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}

    global expenses
    if edit_index is not None:  # Update existing entry
        expenses.iloc[edit_index] = new_expense
        messagebox.showinfo("Success", "Expense updated successfully!")
    else:  # Add new entry
        expenses = pd.concat([expenses, pd.DataFrame([new_expense])], ignore_index=True)
        messagebox.showinfo("Success", "Expense added successfully!")

    clear_entries()
    update_expense_list()
    save_expenses()  # Save data after adding or updating

# Function to update the expense list display
def update_expense_list(month_filter=None):
    for row in expense_tree.get_children():
        expense_tree.delete(row)
    
    filtered_expenses = expenses

    if month_filter:
        filtered_expenses = expenses[expenses['Date'].str.startswith(month_filter)]

    for index, row in filtered_expenses.iterrows():
        expense_tree.insert('', 'end', values=(row['Date'], row['Category'], row['Amount'], row['Description']), iid=index)

# Function to clear input fields
def clear_entries():
    date_entry.set(datetime.now().strftime("%Y-%m-%d"))
    category_combobox.set('')
    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    add_button.config(text="Add Expense", command=lambda: add_or_update_expense())

# Function to handle selection in the list
def on_select(event):
    selected_item = expense_tree.selection()
    if selected_item:
        index = int(selected_item[0])
        selected_expense = expenses.iloc[index]
        date_entry.set(selected_expense['Date'])
        category_combobox.set(selected_expense['Category'])
        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, selected_expense['Amount'])
        description_entry.delete(0, tk.END)
        description_entry.insert(0, selected_expense['Description'])
        add_button.config(text="Update Expense", command=lambda: add_or_update_expense(index))

# Function to delete a selected expense
def delete_expense():
    selected_item = expense_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an expense to delete.")
        return

    index = int(selected_item[0])
    global expenses
    expenses = expenses.drop(index).reset_index(drop=True)
    update_expense_list(month_combobox.get())
    save_expenses()  # Save data after deletion
    messagebox.showinfo("Success", "Expense deleted successfully!")

# Function to plot expense summary
def show_summary():
    if expenses.empty:
        messagebox.showinfo("No Data", "No expenses to display.")
        return
    
    month_filter = month_combobox.get()
    filtered_expenses = expenses

    if month_filter:
        filtered_expenses = expenses[expenses['Date'].str.startswith(month_filter)]

    if filtered_expenses.empty:
        messagebox.showinfo("No Data", f"No expenses found for {month_filter}.")
        return

    category_summary = filtered_expenses.groupby('Category')['Amount'].sum()
    category_summary.plot(kind='bar', title=f'Expense Summary for {month_filter or "All Time"}')
    plt.xlabel('Category')
    plt.ylabel('Amount Spent')
    plt.show()

# Function to generate a PDF report
def generate_pdf(expense_data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.darkblue)
    c.drawString(30, height - 30, f"Expense Report - {datetime.now().strftime('%Y-%m-%d')}")
    c.line(30, height - 35, width - 30, height - 35)

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.black)
    columns = ['Date', 'Category', 'Amount', 'Description']
    x_offset = 30
    y_offset = height - 60

    # Print headers
    for col in columns:
        c.drawString(x_offset, y_offset, col)
        x_offset += 110

    y_offset -= 20
    x_offset = 30

    # Print rows
    for _, row in expense_data.iterrows():
        for item in row:
            c.drawString(x_offset, y_offset, str(item))
            x_offset += 110
        y_offset -= 20
        x_offset = 30

        # Add a new page if necessary
        if y_offset < 50:
            c.showPage()
            c.setFont("Helvetica-Bold", 12)
            y_offset = height - 50

    # Add Total Expenses
    total_expense = expense_data['Amount'].sum()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, y_offset - 20, f"Total Expenses for the Period: ${total_expense:.2f}")

    c.save()

# Function to download expenses as PDF
def download_expenses():
    month_filter = month_combobox.get()
    filtered_expenses = expenses

    if month_filter:
        filtered_expenses = expenses[expenses['Date'].str.startswith(month_filter)]

    if filtered_expenses.empty:
        messagebox.showinfo("No Data", f"No expenses to download for {month_filter}.")
        return

    filename = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[("PDF Files", "*.pdf")])
    if filename:
        generate_pdf(filtered_expenses, filename)
        messagebox.showinfo("Success", f"Expenses saved to {filename}")

# Function to style the GUI
def apply_styles():
    style = ttk.Style()
    style.theme_use("clam")  # Use a clean, professional theme
    style.configure("TLabel", font=("Helvetica", 12), padding=5)
    style.configure("TButton", font=("Helvetica", 12), padding=5, relief="raised", background="lightgrey")
    style.configure("TEntry", padding=5)
    style.configure("TCombobox", padding=5)
    style.configure("Treeview.Heading", font=("Helvetica-Bold", 12), background="#d9d9d9")
    style.configure("Treeview", font=("Helvetica", 12), rowheight=25)

# Create the main window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("800x700")
apply_styles()  # Apply custom styles

# Expense Input Frame
input_frame = ttk.LabelFrame(root, text="Add / Update Expense")
input_frame.pack(pady=10, padx=10, fill='x')

# Date Input
ttk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
date_entry_widget = ttk.Entry(input_frame, textvariable=date_entry)
date_entry_widget.grid(row=0, column=1, padx=5, pady=5)

# Category Input
ttk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
category_combobox = ttk.Combobox(input_frame, values=["Food", "Transport", "Rent", "Entertainment", "Utilities", "Other"])
category_combobox.grid(row=1, column=1, padx=5, pady=5)

# Amount Input
ttk.Label(input_frame, text="Amount ($):").grid(row=2, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(input_frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

# Description Input
ttk.Label(input_frame, text="Description:").grid(row=3, column=0, padx=5, pady=5)
description_entry = ttk.Entry(input_frame)
description_entry.grid(row=3, column=1, padx=5, pady=5)

# Add/Update Expense Button
add_button = ttk.Button(input_frame, text="Add Expense", command=lambda: add_or_update_expense())
add_button.grid(row=4, column=0, columnspan=2, pady=10)

# Filter by Month Frame
filter_frame = ttk.LabelFrame(root, text="Filter by Month")
filter_frame.pack(pady=10, padx=10, fill='x')

# Month Input
ttk.Label(filter_frame, text="Month (YYYY-MM):").pack(padx=5, pady=5, side='left')
month_combobox = ttk.Combobox(filter_frame, values=[f"{datetime.now().year}-{str(i).zfill(2)}" for i in range(1, 13)])
month_combobox.pack(padx=5, pady=5, side='left')

# Filter Button
filter_button = ttk.Button(filter_frame, text="Filter", command=lambda: update_expense_list(month_combobox.get()))
filter_button.pack(padx=5, pady=5, side='left')

# Reset Filter Button
reset_button = ttk.Button(filter_frame, text="Reset", command=lambda: update_expense_list())
reset_button.pack(padx=5, pady=5, side='left')

# Expense List Frame
list_frame = ttk.LabelFrame(root, text="Expense List")
list_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Expense List Treeview
columns = ('Date', 'Category', 'Amount', 'Description')
expense_tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
for col in columns:
    expense_tree.heading(col, text=col)
    expense_tree.column(col, anchor='center')

expense_tree.bind('<<TreeviewSelect>>', on_select)
expense_tree.pack(fill='both', expand=True)

# Delete Expense Button
delete_button = ttk.Button(root, text="Delete Selected Expense", command=delete_expense)
delete_button.pack(pady=10)

# Summary and Download Buttons Frame
button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# Summary Button
summary_button = ttk.Button(button_frame, text="Show Summary", command=show_summary)
summary_button.pack(side='left', padx=10)

# Download Button
download_button = ttk.Button(button_frame, text="Download as PDF", command=download_expenses)
download_button.pack(side='left', padx=10)

# Load the expenses into the treeview
update_expense_list()

# Start the GUI event loop
root.mainloop()
