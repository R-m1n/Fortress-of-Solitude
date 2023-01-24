from abc import ABC, abstractmethod


class Mortgage(ABC):
    MONTHS = 12

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0) -> None:
        self.home_value = home_value

        self.down_payment = self.home_value * down_payment if down_payment < 1 \
            else down_payment

        self.loan_amount = self.home_value - self.down_payment

        self.monthly_interest = interest_rate / self.MONTHS

        self.total_months = loan_term * self.MONTHS

    def annual_payment(self):
        return round(self.monthly_payment() * self.MONTHS, 2)

    def total_payment(self):
        return round(self.monthly_payment() * self.total_months, 2)

    def total_interest(self):
        return self.total_payment() - self.loan_amount

    @abstractmethod
    def monthly_payment(self):
        pass

    @abstractmethod
    def calculate(self):
        pass


class FixedMortgage(Mortgage):

    def monthly_payment(self):
        numerator = self.monthly_interest * \
            (1 + self.monthly_interest) ** self.total_months

        denominator = (1 + self.monthly_interest) ** self.total_months - 1

        return round(self.loan_amount * numerator / denominator, 2)

    def calculate(self):
        pass


fm = FixedMortgage(400_000, .067, 30, 0.2)
print(fm.total_interest())
