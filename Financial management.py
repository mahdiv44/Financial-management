
import json
import os
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

DATA_FILE = "finance_data.json"
SAVINGS_FILE = "savings_data.json"
GOALS_FILE = "goals_data.json"

def load_data(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showerror("خطا", f"خطا در بارگذاری فایل {file_path}: {str(e)}")
            return []
    return []

def save_data(data, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("خطا", f"خطا در ذخیره فایل {file_path}: {str(e)}")

def generate_id(data):
    return data[-1]["id"] + 1 if data else 1

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class FinanceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت مالی")
        self.data = load_data(DATA_FILE)
        self.savings = load_data(SAVINGS_FILE)
        self.goals = load_data(GOALS_FILE)
        self.style = ttk.Style("darkly")
        # تنظیم فونت B Nazanin برای پشتیبانی از فارسی
        self.style.configure("TLabel", font=("B Nazanin", 14))
        self.style.configure("TButton", font=("B Nazanin", 12))
        self.style.configure("TEntry", font=("B Nazanin", 12))
        self.style.configure("Treeview", font=("B Nazanin", 11))
        self.style.configure("Treeview.Heading", font=("B Nazanin", 12, "bold"))
        self.style.configure("success.Treeview", background="#28a745", foreground="white")
        self.style.configure("danger.Treeview", background="#dc3545", foreground="white")
        self.current_frame = None
        self.show_main_menu()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = ttk.Frame(self.root, padding="20")
        self.current_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def show_main_menu(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="مدیریت مالی", font=("B Nazanin", 26, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Button(self.current_frame, text="ثبت تراکنش جدید", command=self.show_add_transaction, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=1, column=0, pady=10)
        ttk.Button(self.current_frame, text="نمایش تراکنش‌ها", command=self.show_transactions, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=2, column=0, pady=10)
        ttk.Button(self.current_frame, text="ویرایش تراکنش", command=self.show_edit_transaction, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=3, column=0, pady=10)
        ttk.Button(self.current_frame, text="حذف تراکنش", command=self.show_delete_transaction, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=4, column=0, pady=10)
        ttk.Button(self.current_frame, text="خلاصه مالی", command=self.show_summary, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=5, column=0, pady=10)
        ttk.Button(self.current_frame, text="مدیریت اهداف مالی", command=self.show_goals, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=6, column=0, pady=10)
        ttk.Button(self.current_frame, text="مدیریت پس‌انداز", command=self.show_savings, bootstyle=(SUCCESS, OUTLINE), width=20).grid(row=7, column=0, pady=10)
        ttk.Button(self.current_frame, text="خروج", command=self.root.quit, bootstyle=(DANGER, OUTLINE), width=20).grid(row=8, column=0, pady=20)

    def show_add_transaction(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="ثبت تراکنش جدید", font=("B Nazanin", 18, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.current_frame, text="نوع تراکنش:").grid(row=1, column=0, sticky=tk.E, padx=5)
        self.type_var = tk.StringVar()
        # فارسی کردن گزینه‌های نوع تراکنش
        ttk.Combobox(self.current_frame, textvariable=self.type_var, values=["درآمد", "هزینه"], state="readonly", bootstyle=SUCCESS).grid(row=1, column=1, pady=5)
        ttk.Label(self.current_frame, text="تاریخ (yyyy-mm-dd):").grid(row=2, column=0, sticky=tk.E, padx=5)
        self.date_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.date_entry.grid(row=2, column=1, pady=5)
        ttk.Label(self.current_frame, text="مبلغ (تومان):").grid(row=3, column=0, sticky=tk.E, padx=5)
        self.amount_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.amount_entry.grid(row=3, column=1, pady=5)
        ttk.Label(self.current_frame, text="دسته‌بندی:").grid(row=4, column=0, sticky=tk.E, padx=5)
        self.category_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.category_entry.grid(row=4, column=1, pady=5)
        ttk.Label(self.current_frame, text="توضیحات:").grid(row=5, column=0, sticky=tk.E, padx=5)
        self.desc_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.desc_entry.grid(row=5, column=1, pady=5)
        ttk.Button(self.current_frame, text="ثبت", command=self.add_transaction, bootstyle=SUCCESS).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=7, column=0, columnspan=2, pady=5)

    def add_transaction(self):
        ttype = self.type_var.get()
        # تبدیل نوع تراکنش فارسی به انگلیسی برای ذخیره‌سازی
        ttype_english = "income" if ttype == "درآمد" else "expense" if ttype == "هزینه" else ""
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        desc = self.desc_entry.get()
        if ttype_english not in ("income", "expense"):
            messagebox.showerror("خطا", "نوع تراکنش نامعتبر است.")
            return
        if not validate_date(date):
            messagebox.showerror("خطا", "فرمت تاریخ نامعتبر است (yyyy-mm-dd).")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("خطا", "مبلغ باید مثبت باشد.")
                return
        except ValueError:
            messagebox.showerror("خطا", "مبلغ نامعتبر است.")
            return
        transaction = {
            "id": generate_id(self.data),
            "date": date,
            "type": ttype_english,
            "amount": amount,
            "category": category,
            "description": desc
        }
        self.data.append(transaction)
        save_data(self.data, DATA_FILE)
        self.update_transaction_list()
        self.clear_entries()
        messagebox.showinfo("موفقیت", "تراکنش با موفقیت ثبت شد!", parent=self.root)
        self.root.update()
        self.show_main_menu()

    def clear_entries(self):
        self.type_var.set("")
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def show_transactions(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="لیست تراکنش‌ها", font=("B Nazanin", 18, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, pady=10)
        self.tree = ttk.Treeview(self.current_frame, columns=("ID", "Date", "Type", "Amount", "Category", "Description"), show="headings", bootstyle=SUCCESS)
        self.tree.heading("ID", text="شناسه")
        self.tree.heading("Date", text="تاریخ")
        self.tree.heading("Type", text="نوع")
        self.tree.heading("Amount", text="مبلغ (تومان)")
        self.tree.heading("Category", text="دسته‌بندی")
        self.tree.heading("Description", text="توضیحات")
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Type", width=80)
        self.tree.column("Amount", width=120)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=150)
        self.tree.grid(row=1, column=0, pady=10)
        self.tree.tag_configure("income", background="#28a745", foreground="white")
        self.tree.tag_configure("expense", background="#dc3545", foreground="white")
        self.update_transaction_list()
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=2, column=0, pady=10)

    def update_transaction_list(self):
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            for t in self.data:
                tag = "income" if t["type"] == "income" else "expense"
                # فارسی کردن نوع تراکنش و افزودن جداکننده سه‌رقمی
                ttype_display = "درآمد" if t["type"] == "income" else "هزینه"
                try:
                    amount_str = f"{t['amount']:,.2f} تومان"
                except (TypeError, ValueError):
                    amount_str = "نامعتبر"
                self.tree.insert("", tk.END, values=(t["id"], t["date"], ttype_display, amount_str, t["category"], t["description"]), tags=(tag,))

    def show_edit_transaction(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="ویرایش تراکنش", font=("B Nazanin", 18, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, pady=10)
        self.tree = ttk.Treeview(self.current_frame, columns=("ID", "Date", "Type", "Amount", "Category", "Description"), show="headings", bootstyle=SUCCESS)
        self.tree.heading("ID", text="شناسه")
        self.tree.heading("Date", text="تاریخ")
        self.tree.heading("Type", text="نوع")
        self.tree.heading("Amount", text="مبلغ (تومان)")
        self.tree.heading("Category", text="دسته‌بندی")
        self.tree.heading("Description", text="توضیحات")
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Type", width=80)
        self.tree.column("Amount", width=120)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=150)
        self.tree.grid(row=1, column=0, pady=10)
        self.tree.tag_configure("income", background="#28a745", foreground="white")
        self.tree.tag_configure("expense", background="#dc3545", foreground="white")
        self.update_transaction_list()
        ttk.Button(self.current_frame, text="ویرایش", command=self.edit_transaction, bootstyle=SUCCESS).grid(row=2, column=0, pady=5)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=3, column=0, pady=5)

    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("خطا", "لطفاً یک تراکنش انتخاب کنید.")
            return
        tid = int(self.tree.item(selected)["values"][0])
        for t in self.data:
            if t["id"] == tid:
                edit_window = ttk.Window(title="ویرایش تراکنش", themename="darkly")
                ttk.Label(edit_window, text="تاریخ (yyyy-mm-dd):", font=("B Nazanin", 14)).grid(row=0, column=0, sticky=tk.E, padx=5)
                date_entry = ttk.Entry(edit_window, bootstyle=SUCCESS)
                date_entry.insert(0, t["date"])
                date_entry.grid(row=0, column=1, pady=5)
                ttk.Label(edit_window, text="نوع تراکنش:", font=("B Nazanin", 14)).grid(row=1, column=0, sticky=tk.E, padx=5)
                type_var = tk.StringVar(value="درآمد" if t["type"] == "income" else "هزینه")
                # فارسی کردن گزینه‌های نوع تراکنش
                ttk.Combobox(edit_window, textvariable=type_var, values=["درآمد", "هزینه"], state="readonly", bootstyle=SUCCESS).grid(row=1, column=1, pady=5)
                ttk.Label(edit_window, text="مبلغ (تومان):", font=("B Nazanin", 14)).grid(row=2, column=0, sticky=tk.E, padx=5)
                amount_entry = ttk.Entry(edit_window, bootstyle=SUCCESS)
                amount_entry.insert(0, f"{t['amount']:.2f}")
                amount_entry.grid(row=2, column=1, pady=5)
                ttk.Label(edit_window, text="دسته‌بندی:", font=("B Nazanin", 14)).grid(row=3, column=0, sticky=tk.E, padx=5)
                category_entry = ttk.Entry(edit_window, bootstyle=SUCCESS)
                category_entry.insert(0, t["category"])
                category_entry.grid(row=3, column=1, pady=5)
                ttk.Label(edit_window, text="توضیحات:", font=("B Nazanin", 14)).grid(row=4, column=0, sticky=tk.E, padx=5)
                desc_entry = ttk.Entry(edit_window, bootstyle=SUCCESS)
                desc_entry.insert(0, t["description"])
                desc_entry.grid(row=4, column=1, pady=5)

                def save_edit():
                    if not validate_date(date_entry.get()):
                        messagebox.showerror("خطا", "فرمت تاریخ نامعتبر است (yyyy-mm-dd).")
                        return
                    ttype = type_var.get()
                    ttype_english = "income" if ttype == "درآمد" else "expense" if ttype == "هزینه" else ""
                    if ttype_english not in ("income", "expense"):
                        messagebox.showerror("خطا", "نوع تراکنش نامعتبر است.")
                        return
                    try:
                        amount = float(amount_entry.get())
                        if amount <= 0:
                            messagebox.showerror("خطا", "مبلغ باید مثبت باشد.")
                            return
                    except ValueError:
                        messagebox.showerror("خطا", "مبلغ نامعتبر است.")
                        return
                    t["date"] = date_entry.get()
                    t["type"] = ttype_english
                    t["amount"] = amount
                    t["category"] = category_entry.get()
                    t["description"] = desc_entry.get()
                    save_data(self.data, DATA_FILE)
                    self.update_transaction_list()
                    messagebox.showinfo("موفقیت", "تراکنش با موفقیت ویرایش شد.")
                    edit_window.destroy()

                ttk.Button(edit_window, text="ذخیره", command=save_edit, bootstyle=SUCCESS).grid(row=5, column=0, columnspan=2, pady=10)
                return
        messagebox.showerror("خطا", "تراکنش پیدا نشد.")

    def show_summary(self):
        self.clear_frame()
        income = sum(t["amount"] for t in self.data if t["type"] == "income")
        expense = sum(t["amount"] for t in self.data if t["type"] == "expense")
        savings = sum(t["amount"] for t in self.savings)
        balance = income - expense - savings
        ttk.Label(self.current_frame, text="خلاصه مالی", font=("B Nazanin", 22, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, pady=20)
        # افزودن جداکننده سه‌رقمی به مبالغ
        ttk.Label(self.current_frame, text=f"کل درآمد (تومان): {income:,.2f}", font=("B Nazanin", 16), bootstyle=SUCCESS).grid(row=1, column=0, pady=10)
        ttk.Label(self.current_frame, text=f"کل هزینه (تومان): {expense:,.2f}", font=("B Nazanin", 16), bootstyle=DANGER).grid(row=2, column=0, pady=10)
        ttk.Label(self.current_frame, text=f"پس‌انداز (تومان): {savings:,.2f}", font=("B Nazanin", 16), bootstyle=INFO).grid(row=3, column=0, pady=10)
        ttk.Label(self.current_frame, text=f"مانده حساب (تومان): {balance:,.2f}", font=("B Nazanin", 16), bootstyle=WARNING).grid(row=4, column=0, pady=10)
        if balance < 0:
            ttk.Label(self.current_frame, text="⚠️ هشدار: مانده حساب منفی است!", font=("B Nazanin", 14), bootstyle=DANGER).grid(row=5, column=0, pady=10)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=6, column=0, pady=20)

    def show_goals(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="مدیریت اهداف مالی", font=("B Nazanin", 22, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, columnspan=2, pady=20)
        ttk.Label(self.current_frame, text="نام هدف:").grid(row=1, column=0, sticky=tk.E, padx=5)
        self.goal_name_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.goal_name_entry.grid(row=1, column=1, pady=5)
        ttk.Label(self.current_frame, text="مبلغ هدف (تومان):").grid(row=2, column=0, sticky=tk.E, padx=5)
        self.goal_amount_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.goal_amount_entry.grid(row=2, column=1, pady=5)
        ttk.Label(self.current_frame, text="مهلت (yyyy-mm-dd):").grid(row=3, column=0, sticky=tk.E, padx=5)
        self.goal_deadline_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.goal_deadline_entry.grid(row=3, column=1, pady=5)
        ttk.Button(self.current_frame, text="افزودن هدف", command=self.add_goal, bootstyle=SUCCESS).grid(row=4, column=0, columnspan=2, pady=10)
        self.tree = ttk.Treeview(self.current_frame, columns=("ID", "Name", "Target", "Progress", "Deadline", "Status"), show="headings", bootstyle=SUCCESS)
        self.tree.heading("ID", text="شناسه")
        self.tree.heading("Name", text="نام هدف")
        self.tree.heading("Target", text="مبلغ هدف (تومان)")
        self.tree.heading("Progress", text="پیشرفت (٪)")
        self.tree.heading("Deadline", text="مهلت")
        self.tree.heading("Status", text="وضعیت")
        self.tree.column("ID", width=50)
        self.tree.column("Name", width=100)
        self.tree.column("Target", width=120)
        self.tree.column("Progress", width=80)
        self.tree.column("Deadline", width=100)
        self.tree.column("Status", width=80)
        self.tree.grid(row=5, column=0, columnspan=2, pady=10)
        self.tree.tag_configure("near_deadline", background="#ffc107", foreground="black")
        self.update_goals_list()
        ttk.Label(self.current_frame, text="مبلغ تخصیص (تومان):").grid(row=6, column=0, sticky=tk.E, padx=5)
        self.allocate_amount_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.allocate_amount_entry.grid(row=6, column=1, pady=5)
        ttk.Label(self.current_frame, text="منبع:").grid(row=7, column=0, sticky=tk.E, padx=5)
        self.allocate_source = tk.StringVar(value="موجودی")
        ttk.Combobox(self.current_frame, textvariable=self.allocate_source, values=["موجودی", "پس‌انداز"], state="readonly", bootstyle=SUCCESS).grid(row=7, column=1, pady=5)
        ttk.Button(self.current_frame, text="تخصیص به هدف", command=self.allocate_to_goal, bootstyle=SUCCESS).grid(row=8, column=0, columnspan=2, pady=10)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=9, column=0, columnspan=2, pady=10)

    def add_goal(self):
        name = self.goal_name_entry.get()
        amount = self.goal_amount_entry.get()
        deadline = self.goal_deadline_entry.get()
        if not name:
            messagebox.showerror("خطا", "نام هدف را وارد کنید.")
            return
        if not validate_date(deadline):
            messagebox.showerror("خطا", "فرمت تاریخ نامعتبر است (yyyy-mm-dd).")
            return
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("خطا", "مبلغ هدف باید مثبت باشد.")
                return
        except ValueError:
            messagebox.showerror("خطا", "مبلغ نامعتبر است.")
            return
        goal = {
            "id": generate_id(self.goals),
            "name": name,
            "target_amount": amount,
            "current_amount": 0.0,
            "deadline": deadline
        }
        self.goals.append(goal)
        save_data(self.goals, GOALS_FILE)
        self.goal_name_entry.delete(0, tk.END)
        self.goal_amount_entry.delete(0, tk.END)
        self.goal_deadline_entry.delete(0, tk.END)
        self.update_goals_list()
        messagebox.showinfo("موفقیت", "هدف مالی با موفقیت اضافه شد!")
        self.show_goals()

    def update_goals_list(self):
        if hasattr(self, 'tree'):
            for item in self.tree.get_children():
                self.tree.delete(item)
            today = datetime.now().date()
            for g in self.goals:
                progress = (g["current_amount"] / g["target_amount"]) * 100 if g["target_amount"] > 0 else 0
                deadline = datetime.strptime(g["deadline"], "%Y-%m-%d").date()
                days_left = (deadline - today).days
                status = "در حال انجام" if days_left > 7 else "مهلت نزدیک!" if days_left > 0 else "منقضی"
                tag = "near_deadline" if days_left <= 7 and days_left > 0 else ""
                # افزودن جداکننده سه‌رقمی به مبلغ هدف
                self.tree.insert("", tk.END, values=(
                    g["id"],
                    g["name"],
                    f"{g['target_amount']:,.2f} تومان",
                    f"{progress:.1f}%",
                    g["deadline"],
                    status
                ), tags=(tag,))

    def allocate_to_goal(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("خطا", "لطفاً یک هدف انتخاب کنید.")
            return
        amount = self.allocate_amount_entry.get()
        source = self.allocate_source.get()
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("خطا", "مبلغ تخصیص باید مثبت باشد.")
                return
        except ValueError:
            messagebox.showerror("خطا", "مبلغ نامعتبر است.")
            return
        tid = int(self.tree.item(selected)["values"][0])
        for g in self.goals:
            if g["id"] == tid:
                if g["current_amount"] + amount > g["target_amount"]:
                    messagebox.showerror("خطا", "مبلغ تخصیص بیش از مبلغ هدف است.")
                    return
                if source == "موجودی":
                    balance = sum(t["amount"] for t in self.data if t["type"] == "income") - sum(t["amount"] for t in self.data if t["type"] == "expense") - sum(t["amount"] for t in self.savings)
                    if amount > balance:
                        messagebox.showerror("خطا", "موجودی کافی نیست.")
                        return
                    expense = {
                        "id": generate_id(self.data),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "expense",
                        "amount": amount,
                        "category": f"هدف: {g['name']}",
                        "description": f"تخصیص به هدف {g['name']}"
                    }
                    self.data.append(expense)
                else:  # پس‌انداز
                    total_savings = sum(t["amount"] for t in self.savings)
                    if amount > total_savings:
                        messagebox.showerror("خطا", "پس‌انداز کافی نیست.")
                        return
                    remaining_amount = amount
                    new_savings = []
                    for s in self.savings:
                        if remaining_amount >= s["amount"]:
                            remaining_amount -= s["amount"]
                        else:
                            s["amount"] -= remaining_amount
                            new_savings.append(s)
                            remaining_amount = 0
                        if remaining_amount <= 0:
                            new_savings.extend(self.savings[self.savings.index(s)+1:])
                            break
                    self.savings = new_savings
                    expense = {
                        "id": generate_id(self.data),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "expense",
                        "amount": amount,
                        "category": f"هدف: {g['name']}",
                        "description": f"تخصیص از پس‌انداز به هدف {g['name']}"
                    }
                    self.data.append(expense)
                g["current_amount"] += amount
                save_data(self.data, DATA_FILE)
                save_data(self.savings, SAVINGS_FILE)
                save_data(self.goals, GOALS_FILE)
                self.allocate_amount_entry.delete(0, tk.END)
                self.update_goals_list()
                messagebox.showinfo("موفقیت", f"{amount:,.2f} تومان به هدف {g['name']} تخصیص یافت.")
                return
        messagebox.showerror("خطا", "هدف پیدا نشد.")

    def show_savings(self):
        self.clear_frame()
        savings = sum(t["amount"] for t in self.savings)
        balance = sum(t["amount"] for t in self.data if t["type"] == "income") - sum(t["amount"] for t in self.data if t["type"] == "expense") - savings
        ttk.Label(self.current_frame, text="مدیریت پس‌انداز", font=("B Nazanin", 22, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, columnspan=2, pady=20)
        # افزودن جداکننده سه‌رقمی به مبالغ
        ttk.Label(self.current_frame, text=f"موجودی پس‌انداز (تومان): {savings:,.2f}", font=("B Nazanin", 16), bootstyle=INFO).grid(row=1, column=0, columnspan=2, pady=10)
        ttk.Label(self.current_frame, text=f"مانده حساب (تومان): {balance:,.2f}", font=("B Nazanin", 16), bootstyle=WARNING).grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Label(self.current_frame, text="مبلغ پس‌انداز (تومان):").grid(row=3, column=0, sticky=tk.E, padx=5)
        self.savings_amount_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.savings_amount_entry.grid(row=3, column=1, pady=5)
        ttk.Button(self.current_frame, text="پس‌انداز", command=self.add_savings, bootstyle=SUCCESS).grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Label(self.current_frame, text="مبلغ رها‌سازی (تومان):").grid(row=5, column=0, sticky=tk.E, padx=5)
        self.release_amount_entry = ttk.Entry(self.current_frame, bootstyle=SUCCESS)
        self.release_amount_entry.grid(row=5, column=1, pady=5)
        ttk.Button(self.current_frame, text="رها‌سازی", command=self.release_savings, bootstyle=WARNING).grid(row=6, column=0, columnspan=2, pady=10)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=7, column=0, columnspan=2, pady=10)

    def add_savings(self):
        amount = self.savings_amount_entry.get()
        try:
            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("خطا", "مبلغ پس‌انداز باید مثبت باشد.")
                return
            balance = sum(t["amount"] for t in self.data if t["type"] == "income") - sum(t["amount"] for t in self.data if t["type"] == "expense") - sum(t["amount"] for t in self.savings)
            if amount > balance:
                messagebox.showerror("خطا", "موجودی کافی نیست.")
                return
            savings_data = {
                "id": generate_id(self.savings),
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.savings.append(savings_data)
            save_data(self.savings, SAVINGS_FILE)
            self.savings_amount_entry.delete(0, tk.END)
            messagebox.showinfo("موفقیت", f"{amount:,.2f} تومان به پس‌انداز اضافه شد.")
            self.show_savings()
        except ValueError:
            messagebox.showerror("خطا", "مبلغ نامعتبر است.")

    def release_savings(self):
        amount = self.release_amount_entry.get()
       
        amount = float(amount)
        if amount <= 0:
                messagebox.showerror("خطا", "مبلغ باید مثبت باشد.")
                return
        total_savings = sum(t["amount"] for t in self.savings)
        if amount > total_savings:
                messagebox.showerror("خطا", "مبلغ رها‌سازی بیش از پس‌انداز است.")
                return
        income_entry = {
                "id": generate_id(self.data),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "type": "income",
                "amount": amount,
                "category": "رها‌سازی پس‌انداز",
                "description": f"رها‌سازی {amount:,.2f} تومان از پس‌انداز"
            }
        self.data.append(income_entry)
        remaining_amount = amount
        new_savings = []
        for s in self.savings:
                if remaining_amount >= s["amount"]:
                    remaining_amount -= s["amount"]
                else:
                    s["amount"] -= remaining_amount
                    new_savings.append(s)
                    remaining_amount = 0
                if remaining_amount <= 0:
                    new_savings.extend(self.savings[self.savings.index(s)+1:])
                    break
        self.savings = new_savings
        save_data(self.data, DATA_FILE)
        save_data(self.savings, SAVINGS_FILE)
        self.release_amount_entry.delete(0, tk.END)
        messagebox.showinfo("موفقیت", f"{amount:,.2f} تومان از پس‌انداز رها شد و به حساب اضافه شد.")
        self.show_savings()

    def show_delete_transaction(self):
        self.clear_frame()
        ttk.Label(self.current_frame, text="حذف تراکنش", font=("B Nazanin", 18, "bold"), bootstyle=SUCCESS).grid(row=0, column=0, pady=10)
        self.tree = ttk.Treeview(self.current_frame, columns=("ID", "Date", "Type", "Amount", "Category", "Description"), show="headings", bootstyle=SUCCESS)
        self.tree.heading("ID", text="شناسه")
        self.tree.heading("Date", text="تاریخ")
        self.tree.heading("Type", text="نوع")
        self.tree.heading("Amount", text="مبلغ (تومان)")
        self.tree.heading("Category", text="دسته‌بندی")
        self.tree.heading("Description", text="توضیحات")
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Type", width=80)
        self.tree.column("Amount", width=120)
        self.tree.column("Category", width=100)
        self.tree.column("Description", width=150)
        self.tree.grid(row=1, column=0, pady=10)
        self.tree.tag_configure("income", background="#28a745", foreground="white")
        self.tree.tag_configure("expense", background="#dc3545", foreground="white")
        self.update_transaction_list()
        ttk.Button(self.current_frame, text="حذف", command=self.delete_transaction, bootstyle=DANGER).grid(row=2, column=0, pady=5)
        ttk.Button(self.current_frame, text="بازگشت", command=self.show_main_menu, bootstyle=(INFO, OUTLINE)).grid(row=3, column=0, pady=5)

    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("خطا", "لطفاً یک تراکنش انتخاب کنید.")
            return
        tid = int(self.tree.item(selected)["values"][0])
        self.data = [t for t in self.data if t["id"] != tid]
        save_data(self.data, DATA_FILE)
        self.update_transaction_list()
        messagebox.showinfo("موفقیت", "تراکنش حذف شد.")

if __name__ == "__main__":
    root = ttk.Window(title="مدیریت مالی", themename="darkly")
    app = FinanceManagerApp(root)
    root.mainloop()
