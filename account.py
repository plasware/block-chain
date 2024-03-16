class Account:
    def __init__(self, account_id, balance=0):
        # 用于创建账户对象，可以指定初始余额。
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        # 存款方法，接受存款金额并将其加到账户余额中。
        if amount > 0:
            self.balance += amount
            return True
        else:
            print("Deposit amount must be greater than 0.")
            return False

    def withdraw(self, amount):
        # 取款方法，接受取款金额并从账户余额中扣除。
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            return True
        else:
            if amount <= 0:
                print("Withdrawal amount must be greater than 0.")
            else:
                print("Insufficient balance for withdrawal.")
            return False

    def get_balance(self):
        # 获取账户余额。
        return self.balance

    def __str__(self):
        return f"Account ID: {self.account_id}, Balance: {self.balance}"