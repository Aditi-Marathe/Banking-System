import tkinter as tk
from tkinter import messagebox

class BankSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏦 Banking System")
        self.root.geometry("600x600")
        
        # New Color Theme
        self.bg_color = "#E6E6FA"  # Light Purple
        self.btn_color = "#3A3FCD"  # Dark Blue
        self.text_color = "#1A1A6B"  # Navy Blue
        self.entry_bg = "#FFFFFF"  # White

        self.root.configure(bg=self.bg_color)

        self.accounts = {}

        # Title Label
        self.title_label = tk.Label(root, text="🏦 Banking System Menu", font=("Arial", 18, "bold"), fg=self.text_color, bg=self.bg_color)
        self.title_label.pack(pady=15)

        # Buttons
        self.create_buttons()

    def create_buttons(self):
        btn_options = {"font": ("Arial", 14, "bold"), "bg": self.btn_color, "fg": "white", "width": 20, "height": 2}

        self.create_account_btn = tk.Button(self.root, text="🆕 Create Account", command=self.create_account, **btn_options)
        self.create_account_btn.pack(pady=8)

        self.deposit_btn = tk.Button(self.root, text="💵 Deposit Money", command=self.deposit_money, **btn_options)
        self.deposit_btn.pack(pady=8)

        self.withdraw_btn = tk.Button(self.root, text="💳 Withdraw Money", command=self.withdraw_money, **btn_options)
        self.withdraw_btn.pack(pady=8)

        self.check_balance_btn = tk.Button(self.root, text="🔍 Check Balance", command=self.check_balance, **btn_options)
        self.check_balance_btn.pack(pady=8)

        self.display_info_btn = tk.Button(self.root, text="📄 Display Account Info", command=self.display_account_info, **btn_options)
        self.display_info_btn.pack(pady=8)

        self.delete_account_btn = tk.Button(self.root, text="❌ Delete Account", command=self.delete_account, **btn_options)
        self.delete_account_btn.pack(pady=8)

        self.exit_btn = tk.Button(self.root, text="🚪 Exit", font=("Arial", 14, "bold"), bg="#C70039", fg="white", width=20, height=2, command=self.root.quit)
        self.exit_btn.pack(pady=15)

    def create_account(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Account 🆕")
        create_window.geometry("400x300")
        create_window.configure(bg=self.bg_color)

        tk.Label(create_window, text="Enter Account Number:", bg=self.bg_color, fg=self.text_color).pack()
        account_number_entry = tk.Entry(create_window, bg=self.entry_bg)
        account_number_entry.pack()

        tk.Label(create_window, text="Enter Account Holder Name:", bg=self.bg_color, fg=self.text_color).pack()
        account_holder_entry = tk.Entry(create_window, bg=self.entry_bg)
        account_holder_entry.pack()

        tk.Label(create_window, text="Enter Initial Balance:", bg=self.bg_color, fg=self.text_color).pack()
        initial_balance_entry = tk.Entry(create_window, bg=self.entry_bg)
        initial_balance_entry.pack()

        def save_account():
            account_number = account_number_entry.get()
            account_holder = account_holder_entry.get()
            initial_balance = initial_balance_entry.get()
            if account_number and account_holder and initial_balance.isdigit():
                self.accounts[account_number] = {"holder": account_holder, "balance": float(initial_balance)}
                messagebox.showinfo("Success", "Account Created Successfully! 🎉")
                create_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid input. Please try again.")

        tk.Button(create_window, text="✅ Create", bg=self.btn_color, fg="white", command=save_account).pack(pady=10)

    def deposit_money(self):
        self.transaction_window("Deposit Money 💵", "Enter Amount to Deposit:", self.deposit)

    def withdraw_money(self):
        self.transaction_window("Withdraw Money 💳", "Enter Amount to Withdraw:", self.withdraw)

    def check_balance(self):
        self.transaction_window("Check Balance 🔍", "Enter Account Number:", self.show_balance)

    def display_account_info(self):
        self.transaction_window("Account Info 📄", "Enter Account Number:", self.show_info)

    def delete_account(self):
        self.transaction_window("Delete Account ❌", "Enter Account Number:", self.remove_account)

    def transaction_window(self, title, label_text, command_function):
        trans_window = tk.Toplevel(self.root)
        trans_window.title(title)
        trans_window.geometry("300x200")
        trans_window.configure(bg=self.bg_color)

        tk.Label(trans_window, text=label_text, bg=self.bg_color, fg=self.text_color).pack()
        account_entry = tk.Entry(trans_window, bg=self.entry_bg)
        account_entry.pack()

        amount_entry = None
        if title != "Check Balance 🔍" and title != "Delete Account ❌":
            tk.Label(trans_window, text="Enter Amount:", bg=self.bg_color, fg=self.text_color).pack()
            amount_entry = tk.Entry(trans_window, bg=self.entry_bg)
            amount_entry.pack()

        def execute():
            command_function(account_entry.get(), amount_entry.get() if amount_entry else None)
            trans_window.destroy()

        tk.Button(trans_window, text="✅ Confirm", bg=self.btn_color, fg="white", command=execute).pack(pady=10)

    def deposit(self, account, amount):
        if account in self.accounts and amount and amount.isdigit():
            self.accounts[account]["balance"] += float(amount)
            messagebox.showinfo("Success", "Deposit Successful! 🎉")
        else:
            messagebox.showerror("Error", "Invalid account or amount.")

    def withdraw(self, account, amount):
        if account in self.accounts and amount and amount.isdigit():
            amount = float(amount)
            if amount <= self.accounts[account]["balance"]:
                self.accounts[account]["balance"] -= amount
                messagebox.showinfo("Success", "Withdrawal Successful! 🎉")
            else:
                messagebox.showerror("Error", "Insufficient Funds!")
        else:
            messagebox.showerror("Error", "Invalid account or amount.")

    def show_balance(self, account, _):
        if account in self.accounts:
            balance = self.accounts[account]["balance"]
            messagebox.showinfo("Balance", f"Account: {account}\nBalance: ₹{balance}")
        else:
            messagebox.showerror("Error", "Account not found!")

    def show_info(self, account, _):
        if account in self.accounts:
            info = self.accounts[account]
            messagebox.showinfo("Account Info", f"Account: {account}\nHolder: {info['holder']}\nBalance: ₹{info['balance']}")
        else:
            messagebox.showerror("Error", "Account not found!")

    def remove_account(self, account, _):
        if account in self.accounts:
            del self.accounts[account]
            messagebox.showinfo("Deleted", "Account Deleted Successfully! ❌")
        else:
            messagebox.showerror("Error", "Account not found!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankSystemGUI(root)
    root.mainloop()
