# Project Description
This project is a Personal Finance Tracker built using Python and Tkinter. It helps users manage and track their expenses efficiently by providing an intuitive graphical user interface (GUI) with features like adding, updating, filtering, and summarizing expenses. The application also offers data visualization and export capabilities for better financial insights.

## Key Features:

Expense Management:

- Add new expenses with details like date, category, amount, and description.
- Edit existing expenses or delete unwanted entries.

## Data Filtering:

- Filter expenses by specific months to view and analyze data easily.

## Expense Summary:

- Visualize spending with bar charts that display category-wise expense summaries.

## Data Persistence:

- All expenses are saved in a CSV file (expenses.csv) for permanent storage.
- Automatically loads saved data on application startup.

## PDF Export:

- Generate and save expense reports as PDF files for offline use.

## Responsive GUI:

- Clean, user-friendly interface built with Tkinter.
- Dynamic table view for browsing, selecting, and managing expenses.
- This project is perfect for individuals seeking a simple, lightweight tool to organize their personal finances and track their spending habits.

# Personal Finance Tracker

## Overview

The **Personal Finance Tracker** is a desktop application designed to help users manage and track their expenses with ease. Built with **Python** and **Tkinter**, this tool provides an intuitive graphical user interface (GUI) to add, update, filter, and summarize expenses. It also supports data export and visualization for better financial management.

---

## Features

### 1. Expense Management
- Add new expenses with details like date, category, amount, and description.
- Edit or delete existing expense entries.

### 2. Data Filtering
- Filter expenses by specific months to focus on particular time periods.

### 3. Expense Summary
- Visualize category-wise spending with bar charts.

### 4. Data Persistence
- Automatically saves all expense data in a CSV file (`expenses.csv`).
- Reloads saved data on application startup.

### 5. PDF Export
- Generate detailed expense reports and save them as PDF files.

### 6. User-Friendly GUI
- Clean and responsive interface for managing expenses.
- Dynamic table view for browsing and selecting records.

---

## Installation

### Clone the Repository
```bash
git clone https://github.com/<your-username>/personal-finance-tracker.git
cd personal-finance-tracker
```

### Install Dependencies

Ensure you have Python 3.7+ installed. Then install the required packages:
```bash
pip install pandas matplotlib reportlab
```

### Run the Application
```bash
python app.py
```

### Usage

- Adding a New Expense
- Enter the date, category, amount, and description in the input fields.
- Click Add Expense to save the entry.
- Updating an Expense
- Select an expense from the table view.
- Edit the details in the input fields.
- Click Update Expense to save the changes.
- Deleting an Expense
- Select an expense from the table view.
- Click Delete Selected Expense to remove it.
- Viewing a Summary
- Select a month using the filter option (optional).
- Click Show Summary to display a bar chart of category-wise expenses.
- Exporting Expenses as PDF
- Filter expenses by month if desired.
- Click Download as PDF and save the file.

### File Structure

![image](https://github.com/user-attachments/assets/994e1893-5086-41e0-b7df-0957ad1c0e9d)

### Dependencies

- Python 3.7+
- pandas: For data management.
- matplotlib: For generating bar charts.
- reportlab: For creating PDF reports.
- Tkinter: Built-in GUI framework for Python.

### Install dependencies using:

```bash
pip install pandas matplotlib reportlab
```

### Future Enhancements

- Add support for income tracking and budget planning.
- Integrate data visualization for trends over time.
- Enable export to additional formats like Excel or JSON.
- Implement multi-user support for shared expense tracking.


