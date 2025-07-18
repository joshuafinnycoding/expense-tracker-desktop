import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use("TkAgg")

CATEGORIES = ["Food", "Transport", "Utilities", "Entertainment", "Other"]

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("800x600")
        self.expenses = []
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Add Expense Tab
        self.add_tab = ttk.Frame(notebook)
        notebook.add(self.add_tab, text="Add Expense")
        self.create_add_expense_tab()

        # View Expenses Tab
        self.view_tab = ttk.Frame(notebook)
        notebook.add(self.view_tab, text="View Expenses")
        self.create_view_expenses_tab()

        # Reports Tab
        self.report_tab = ttk.Frame(notebook)
        notebook.add(self.report_tab, text="Reports")
        self.create_reports_tab()

    def create_add_expense_tab(self):
        frame = self.add_tab

        ttk.Label(frame, text="Description:").grid(row=0, column=0, sticky="e")
        self.desc_entry = ttk.Entry(frame, width=40)
        self.desc_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Amount:").grid(row=1, column=0, sticky="e")
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category:").grid(row=2, column=0, sticky="e")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(frame, textvariable=self.category_var, values=CATEGORIES, state="readonly")
        self.category_combo.grid(row=2, column=1, padx=5, pady=5)
        self.category_combo.current(0)

        ttk.Label(frame, text="Date:").grid(row=3, column=0, sticky="e")
        self.date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Notes:").grid(row=4, column=0, sticky="e")
        self.notes_entry = ttk.Entry(frame, width=40)
        self.notes_entry.grid(row=4, column=1, padx=5, pady=5)

        add_btn = ttk.Button(frame, text="Add Expense", command=self.add_expense)
        add_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def create_view_expenses_tab(self):
        frame = self.view_tab

        columns = ("Description", "Amount", "Category", "Date", "Notes")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=5)
        edit_btn = ttk.Button(btn_frame, text="Edit", command=self.edit_expense)
        edit_btn.pack(side="left", padx=5)
        del_btn = ttk.Button(btn_frame, text="Delete", command=self.delete_expense)
        del_btn.pack(side="left", padx=5)

    def create_reports_tab(self):
        frame = self.report_tab
        self.report_canvas = None
        self.update_report_chart()

    def add_expense(self):
        desc = self.desc_entry.get()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Amount must be a number.")
            return
        category = self.category_var.get()
        date = self.date_entry.get_date()
        notes = self.notes_entry.get()

        expense = {
            "Description": desc,
            "Amount": amount,
            "Category": category,
            "Date": date,
            "Notes": notes
        }
        self.expenses.append(expense)
        self.refresh_expense_table()
        self.update_report_chart()
        self.clear_add_form()

    def clear_add_form(self):
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_combo.current(0)
        self.date_entry.set_date(datetime.date.today())
        self.notes_entry.delete(0, tk.END)

    def refresh_expense_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for idx, exp in enumerate(self.expenses):
            self.tree.insert("", "end", iid=idx, values=(
                exp["Description"], exp["Amount"], exp["Category"], exp["Date"], exp["Notes"]
            ))

    def edit_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Expense", "Please select an expense to edit.")
            return
        idx = int(selected[0])
        exp = self.expenses[idx]

        # Simple edit dialog
        edit_win = tk.Toplevel(self)
        edit_win.title("Edit Expense")
        edit_win.grab_set()

        ttk.Label(edit_win, text="Description:").grid(row=0, column=0)
        desc_entry = ttk.Entry(edit_win, width=40)
        desc_entry.insert(0, exp["Description"])
        desc_entry.grid(row=0, column=1)

        ttk.Label(edit_win, text="Amount:").grid(row=1, column=0)
        amount_entry = ttk.Entry(edit_win)
        amount_entry.insert(0, str(exp["Amount"]))
        amount_entry.grid(row=1, column=1)

        ttk.Label(edit_win, text="Category:").grid(row=2, column=0)
        category_var = tk.StringVar(value=exp["Category"])
        category_combo = ttk.Combobox(edit_win, textvariable=category_var, values=CATEGORIES, state="readonly")
        category_combo.grid(row=2, column=1)
        category_combo.set(exp["Category"])

        ttk.Label(edit_win, text="Date:").grid(row=3, column=0)
        date_entry = DateEntry(edit_win)
        date_entry.set_date(exp["Date"])
        date_entry.grid(row=3, column=1)

        ttk.Label(edit_win, text="Notes:").grid(row=4, column=0)
        notes_entry = ttk.Entry(edit_win, width=40)
        notes_entry.insert(0, exp["Notes"])
        notes_entry.grid(row=4, column=1)

        def save_edit():
            try:
                new_amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Amount must be a number.")
                return
            self.expenses[idx] = {
                "Description": desc_entry.get(),
                "Amount": new_amount,
                "Category": category_var.get(),
                "Date": date_entry.get_date(),
                "Notes": notes_entry.get()
            }
            self.refresh_expense_table()
            self.update_report_chart()
            edit_win.destroy()

        save_btn = ttk.Button(edit_win, text="Save", command=save_edit)
        save_btn.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Select Expense", "Please select an expense to delete.")
            return
        idx = int(selected[0])
        if messagebox.askyesno("Delete", "Are you sure you want to delete this expense?"):
            del self.expenses[idx]
            self.refresh_expense_table()
            self.update_report_chart()

    def update_report_chart(self):
        # Monthly spend summary
        monthly = {}
        for exp in self.expenses:
            month = exp["Date"].strftime("%Y-%m")
            monthly[month] = monthly.get(month, 0) + exp["Amount"]

        months = sorted(monthly.keys())
        amounts = [monthly[m] for m in months]

        fig = Figure(figsize=(6, 4))
        ax = fig.add_subplot(111)
        ax.bar(months, amounts)
        ax.set_title("Monthly Spend Summary")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Spent")

        if self.report_canvas:
            self.report_canvas.get_tk_widget().destroy()
        self.report_canvas = FigureCanvasTkAgg(fig, master=self.report_tab)
        self.report_canvas.draw()
        self.report_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()