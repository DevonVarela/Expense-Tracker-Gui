# Personal Expense Tracker - Devon Varela - BUS472

# imports tkinter for the GUI window and widgets
# Source: https://docs.python.org/3/library/tkinter.html
import tkinter as tk
from tkinter import messagebox  # messagebox gives us popup dialogs for errors and warnings

# my own list of categories the user can pick from
CATEGORIES = ["Food", "Transport", "Entertainment", "Shopping", "Health", "Other"]

# creates the main application window
# Source: https://www.geeksforgeeks.org/python-gui-tkinter/
root = tk.Tk()
root.title("Personal Expense Tracker")  # sets the text in the title bar
root.geometry("500x580")                # sets the window size in pixels
root.resizable(False, False)            # locks the window so it cannot be resized
root.configure(bg="#f0f4f8")            # my own background color for a cleaner look

# my own list to store each expense as a dictionary
expenses = []

# StringVar variables link the input fields to Python variables so we can read them easily
desc_var = tk.StringVar()
amount_var = tk.StringVar()
category_var = tk.StringVar(value=CATEGORIES[0])  # defaults the dropdown to the first category


# MY CODE: this function runs when the user clicks Add Expense
# it validates the input, saves the expense, and updates the display
def add_expense():
    desc = desc_var.get().strip()         # reads the description field and removes extra spaces
    amount_text = amount_var.get().strip() # reads the amount field
    category = category_var.get()          # reads the selected category from the dropdown

    # my own check: shows a warning if either field was left empty
    if not desc or not amount_text:
        messagebox.showwarning("Missing Info", "Please enter both a description and an amount.")
        return

    # my own check: tries to convert amount to a number, shows error if it fails
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Invalid Amount", "Amount must be a positive number.")
        return

    # my own code: stores the expense as a dictionary in the expenses list
    expenses.append({"desc": desc, "amount": amount, "category": category})

    # formats the text so category, amount, and description line up in columns
    # Source: https://www.tutorialspoint.com/python/tk_listbox.htm
    display_text = f"  {category:<14}  ${amount:>7.2f}   {desc}"
    expense_listbox.insert(tk.END, display_text)  # adds the entry to the bottom of the listbox

    # my own code: alternates row colors so the list is easier to read
    if len(expenses) % 2 == 0:
        expense_listbox.itemconfig(tk.END, bg="#dce8f5")
    else:
        expense_listbox.itemconfig(tk.END, bg="#ffffff")

    update_total()       # recalculates and refreshes the total at the bottom
    desc_var.set("")     # clears the description field for the next entry
    amount_var.set("")   # clears the amount field for the next entry


# MY CODE: adds up all expense amounts and updates the total label
def update_total():
    total = sum(e["amount"] for e in expenses)  # loops through expenses list and sums the amounts
    total_label.config(text=f"Total Spent:   ${total:.2f}")  # updates the label with the new total


# MY CODE: clears all expenses after asking the user to confirm
def clear_expenses():
    if not expenses:  # does nothing if the list is already empty
        return
    if messagebox.askyesno("Clear All", "Are you sure you want to clear all expenses?"):
        expenses.clear()                    # empties the Python list
        expense_listbox.delete(0, tk.END)   # removes all items from the listbox widget
        update_total()                      # resets the total back to $0.00


# creates the title label at the top of the window
# Source: https://www.geeksforgeeks.org/python-gui-tkinter/
title_label = tk.Label(root, text="Personal Expense Tracker",
                       font=("Helvetica", 18, "bold"), bg="#f0f4f8", fg="#2c3e50")
title_label.pack(pady=(16, 6))

# frame to group the three input fields together
input_frame = tk.Frame(root, bg="#f0f4f8", padx=20)
input_frame.pack(fill="x")

# Description label and text entry field
tk.Label(input_frame, text="Description:", bg="#f0f4f8", font=("Helvetica", 11)).grid(row=0, column=0, sticky="w", pady=4)
desc_entry = tk.Entry(input_frame, textvariable=desc_var, font=("Helvetica", 11), width=32)
desc_entry.grid(row=0, column=1, pady=4, padx=(8, 0))

# Amount label and text entry field
tk.Label(input_frame, text="Amount ($):", bg="#f0f4f8", font=("Helvetica", 11)).grid(row=1, column=0, sticky="w", pady=4)
amount_entry = tk.Entry(input_frame, textvariable=amount_var, font=("Helvetica", 11), width=32)
amount_entry.grid(row=1, column=1, pady=4, padx=(8, 0))

# Category label and dropdown menu
tk.Label(input_frame, text="Category:", bg="#f0f4f8", font=("Helvetica", 11)).grid(row=2, column=0, sticky="w", pady=4)

# OptionMenu creates the dropdown that shows the CATEGORIES list
# Source: https://www.tutorialspoint.com/python/tk_optionmenu.htm
category_menu = tk.OptionMenu(input_frame, category_var, *CATEGORIES)
category_menu.config(font=("Helvetica", 11), width=28, bg="#ffffff")
category_menu.grid(row=2, column=1, pady=4, padx=(8, 0), sticky="w")

# my own frame to place both buttons side by side
btn_frame = tk.Frame(root, bg="#f0f4f8")
btn_frame.pack(pady=10)

# blue Add Expense button calls add_expense() when clicked
add_btn = tk.Button(btn_frame, text="Add Expense", command=add_expense,
                    font=("Helvetica", 11, "bold"), bg="#3498db", fg="white",
                    padx=14, pady=6, relief="flat")
add_btn.grid(row=0, column=0, padx=8)

# my own red color for Clear All to signal it is a destructive action
clear_btn = tk.Button(btn_frame, text="Clear All", command=clear_expenses,
                      font=("Helvetica", 11), bg="#e74c3c", fg="white",
                      padx=14, pady=6, relief="flat")
clear_btn.grid(row=0, column=1, padx=8)

# dark header bar above the list showing column names in monospace font
header_label = tk.Label(root, text=f"  {'Category':<14}  {'Amount':>9}   Description",
                        font=("Courier", 10, "bold"), bg="#2c3e50", fg="white",
                        anchor="w", padx=10)
header_label.pack(fill="x", padx=20)

# frame to hold the listbox and scrollbar together
list_frame = tk.Frame(root, bg="#f0f4f8")
list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 6))

# scrollbar linked to the listbox so they scroll together
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

# listbox displays all added expenses in a scrollable list
# Source: https://www.tutorialspoint.com/python/tk_listbox.htm
expense_listbox = tk.Listbox(list_frame, font=("Courier", 11),
                              yscrollcommand=scrollbar.set,
                              selectbackground="#3498db",
                              height=12, relief="flat", bd=0)
expense_listbox.pack(fill="both", expand=True)
scrollbar.config(command=expense_listbox.yview)  # connects scrollbar movement to the listbox

# my own dark footer bar that shows the running total in green text
total_label = tk.Label(root, text="Total Spent:   $0.00",
                       font=("Helvetica", 14, "bold"), bg="#2c3e50", fg="#2ecc71", pady=10)
total_label.pack(fill="x", padx=20, pady=(0, 16))

# starts the event loop - keeps the window open and listens for user interactions
# Source: https://docs.python.org/3/library/tkinter.html
root.mainloop()