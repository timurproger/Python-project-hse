import re
from datetime import datetime


class Operation:
    def __init__(
        self,
        date: datetime,
        type_operation: str,
        account_number: str,
        amount: float,
        balance: float,
        status: str,
    ):
        self.date = date
        self.type_operation = type_operation
        self.account_number = account_number
        self.status = status
        self.balance = balance
        self.amount = amount

    def to_dict(self):
        return {
            "date": self.date.isoformat(),
            "type_operation": self.type_operation,
            "account_number": self.account_number,
            "status": self.status,
            "balance": self.balance,
            "amount": self.amount,
        }

class AccountBank():
    __account_counter = 1000
    __balance = 0

    def __init__(self, account_holder, balance=0, account_number=None):
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")

        if not self.__validate_holder(account_holder):
            raise ValueError(
                "Имя должно быть в формате 'Имя Фамилия' "
                "с заглавных букв"
            )

        if account_number != None:
            account_num = self.account_number = f'ACC-{account_number}'
        else:
            AccountBank.__account_counter += 1
            account_num = AccountBank.__account_counter

        self.holder = account_holder
        self.__balance = balance
        self.account_number = f'ACC-{account_num}'
        self.operations_history = []

    def deposit(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Пополнения не могут быть меньше 0")

        self.__balance += amount
        op = Operation(type_operation='deposit', account_number=self.account_number, status='success',
                       date=datetime.now(), balance=self.__balance, amount=amount)
        self.operations_history.append(op)


    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")
        if amount <= 0:
            raise ValueError("Снятие не могут быть отрицательными")
        if amount > self.__balance:
            op = Operation(type_operation='withdraw', account_number=self.account_number, status='fail',
                           date=datetime.now(), balance=self.__balance, amount=amount)
            self.operations_history.append(op)
            raise ValueError("Снятие не могут быть больше баланса")

        self.__balance -= amount
        op = Operation(type_operation='withdraw', account_number=self.account_number, status='success',
                       date=datetime.now(), balance=self.__balance, amount=amount)
        self.operations_history.append(op)

    def __validate_holder(self, holder):
        pattern = r"^[A-ZА-ЯЁ][a-zа-яё]+ [A-ZА-ЯЁ][a-zа-яё]+$"
        return re.fullmatch(pattern, holder) is not None

    def get_balance(self):
        return self.__balance

    def get_history(self):
        return [i.to_dict() for i in self.operations_history]


class CheckingAccount(AccountBank):
    account_type = "checking"


class SavingsAccount(AccountBank):
    account_type = 'savings'

    def withdraw(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("Сумма должна быть числом")

        balance = self.get_balance()

        if amount > balance * 0.5:
            op = Operation(type_operation='withdraw', account_number=self.account_number, status='fail',
                           date=datetime.now(), balance=balance, amount=amount)
            self.operations_history.append(op)
            raise ValueError("Нельзя снимать с сберегательного счета больше 50%")

        super().withdraw(amount)

    def apply_interest(self, rate):
        if not isinstance(rate, (int, float)):
            raise TypeError("Процент должен быть числом")

        if rate < 0:
            raise ValueError(
                "Процент не может быть отрицательным"
            )

        interest = self.get_balance() * rate / 100

        self.deposit(interest)


client_1 = CheckingAccount(
    "Петр Иванов",
    100
)

client_2 = SavingsAccount(
    "Михаил Петров",
    1000
)

client_1.deposit(100)

print(client_1.get_balance())
# 200

client_1.withdraw(50)

print(client_1.get_balance())
# 150

print(client_1.get_history())

print(client_2.get_balance())
# 1000

client_2.withdraw(400)

print(client_2.get_balance())
# 600
