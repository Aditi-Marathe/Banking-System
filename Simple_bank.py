import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

class InsufficientFundsError(Exception):
    """Custom exception for insufficient funds."""
    pass

class Account:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance
        self.transactions = []  # Store transaction history

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transactions.append(f'✅ Deposited: {amount}')
        else:
            raise ValueError("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(f"❌ Insufficient funds. Available balance: {self.balance}.")
        elif amount > 0:
            self.balance -= amount
            self.transactions.append(f'💸 Withdrawn: {amount}')
        else:
            raise ValueError("Withdrawal amount must be positive.")

    def get_balance(self):
        return self.balance

    def display_account_info(self):
        return f"🏦 Account Number: {self.account_number}\n👤 Account Holder: {self.account_holder}\n💰 Balance: {self.balance}"

    def get_transaction_history(self):
        return '\n'.join(self.transactions) if self.transactions else "No transactions yet."

class BankingSystem:
    def __init__(self, root):
        self.accounts = {}
        self.root = root
        self.root.title("🏦 Banking System")
        self.root.geometry("800x600")

        # Widgets for account creation
        self.create_account_frame = tb.Frame(root)
        self.create_account_frame.pack(pady=10)

        tb.Label(self.create_account_frame, text="🔢 Account Number:").grid(row=0, column=0)
        self.acc_num_entry = tb.Entry(self.create_account_frame)
        self.acc_num_entry.grid(row=0, column=1)
    
        tb.Label(self.create_account_frame, text="👤 Account Holder:").grid(row=1, column=0)
        self.acc_holder_entry = tb.Entry(self.create_account_frame)
        self.acc_holder_entry.grid(row=1, column=1)
    
        tb.Label(self.create_account_frame, text="💰 Initial Balance:").grid(row=2, column=0)
        self.initial_balance_entry = tb.Entry(self.create_account_frame)
        self.initial_balance_entry.grid(row=2, column=1)
    
        self.create_account_button = tb.Button(self.create_account_frame, text="📜 Create Account", command=self.create_account, bootstyle="success")
        self.create_account_button.grid(row=3, columnspan=2, pady=5)
    
        # Transaction Section
        self.transaction_frame = tb.Frame(root)
        self.transaction_frame.pack(pady=10)

        tb.Label(self.transaction_frame, text="🔢 Enter Account Number:").grid(row=0, column=0)
        self.trans_acc_num_entry = tb.Entry(self.transaction_frame)
        self.trans_acc_num_entry.grid(row=0, column=1)

        tb.Label(self.transaction_frame, text="💵 Enter Amount:").grid(row=1, column=0)
        self.amount_entry = tb.Entry(self.transaction_frame)
        self.amount_entry.grid(row=1, column=1)
    
        self.deposit_button = tb.Button(self.transaction_frame, text="💰 Deposit", command=self.deposit, bootstyle="primary")
        self.deposit_button.grid(row=2, column=0, pady=5)
    
        self.withdraw_button = tb.Button(self.transaction_frame, text="💸 Withdraw", command=self.withdraw, bootstyle="danger")
        self.withdraw_button.grid(row=2, column=1, pady=5)
    
        # Account Info Section
        self.info_frame = tb.Frame(root)
        self.info_frame.pack(pady=10)
    
        tb.Label(self.info_frame, text="🔎 Enter Account Number:").grid(row=0, column=0)
        self.info_acc_num_entry = tb.Entry(self.info_frame)
        self.info_acc_num_entry.grid(row=0, column=1)
    
        self.check_balance_button = tb.Button(self.info_frame, text="💳 Check Balance", command=self.display_info, bootstyle="info")
        self.check_balance_button.grid(row=1, column=0, pady=5)
    
        self.history_button = tb.Button(self.info_frame, text="📜 Transaction History", command=self.show_transaction_history, bootstyle="warning")
        self.history_button.grid(row=1, column=1, pady=5)
    
    def create_account(self):
        acc_num = self.acc_num_entry.get().strip()
        acc_holder = self.acc_holder_entry.get().strip()
        try:
            initial_balance = float(self.initial_balance_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Initial balance must be a number!")
            return
    
        if not acc_num or not acc_holder:
            messagebox.showwarning("Error", "Account number and holder name cannot be empty!")
            return
        if initial_balance < 0:
            messagebox.showwarning("Error", "Initial balance must be positive!")
            return
    
        if acc_num in self.accounts:
            messagebox.showwarning("Error", "Account number already exists!")
            return
    
        self.accounts[acc_num] = Account(acc_num, acc_holder, initial_balance)
        messagebox.showinfo("Success", "🎉 Account created successfully!")
        self.clear_entries([self.acc_num_entry, self.acc_holder_entry, self.initial_balance_entry])
    
    def deposit(self):
        self.process_transaction("deposit")
    
    def withdraw(self):
        self.process_transaction("withdraw")
    
    def process_transaction(self, transaction_type):
        acc_num = self.trans_acc_num_entry.get().strip()
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Error", "Amount must be a number!")
            return
    
        if acc_num not in self.accounts:
            messagebox.showwarning("Error", "Account not found!")
            return
    
        try:
            if transaction_type == "deposit":
                self.accounts[acc_num].deposit(amount)
            else:
                self.accounts[acc_num].withdraw(amount)
            messagebox.showinfo("Success", f"✅ Transaction successful! New balance: {self.accounts[acc_num].get_balance()}")
        except (InsufficientFundsError, ValueError) as e:
            messagebox.showwarning("Error", str(e))
    
    def display_info(self):
        acc_num = self.info_acc_num_entry.get().strip()
        if acc_num in self.accounts:
            messagebox.showinfo("Account Info", self.accounts[acc_num].display_account_info())
        else:
            messagebox.showwarning("Error", "Account not found!")
    
    def show_transaction_history(self):
        acc_num = self.info_acc_num_entry.get().strip()
        if acc_num in self.accounts:
            messagebox.showinfo("Transaction History", self.accounts[acc_num].get_transaction_history())
        else:
            messagebox.showwarning("Error", "Account not found!")
    
    def clear_entries(self, entries):
        for entry in entries:
            entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tb.Window(themename="minty")
    app = BankingSystem(root)
    root.mainloop()
