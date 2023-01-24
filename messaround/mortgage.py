from abc import ABC, abstractmethod


class Mortgage(ABC):
    MONTHS = 12

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0) -> None:
        self.home_value = home_value

        self.down_payment = self.home_value * (down_payment / 100) if down_payment < 100 \
            else down_payment

        self.loan_amount = self.home_value - self.down_payment

        self.monthly_interest = interest_rate / self.MONTHS

        self.total_months = loan_term * self.MONTHS

    def annual_payment(self):
        return round(self.monthly_payment() * self.MONTHS, 2)

    def total_payment(self):
        return round(self.monthly_payment() * self.total_months, 2)

    def total_interest(self):
        return round(self.total_payment() - self.loan_amount, 2)

    @abstractmethod
    def monthly_payment(self):
        pass

    @abstractmethod
    def calculate(self):
        pass


class FixedMortgage(Mortgage):
    DISCOUNT_PER_POINT = .0025

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0, points: int | float = 0) -> None:
        interest_rate = (interest_rate / 100) - \
            (points * self.DISCOUNT_PER_POINT)

        super().__init__(home_value, interest_rate, loan_term, down_payment)

        self.points = points

        self.prepaid_interest = self.loan_amount * (points / 100)

        self.point_cost = (self.loan_amount * (points / 100)) / points \
            if points > 0 else 0

    def monthly_payment(self):
        numerator = self.monthly_interest * \
            (1 + self.monthly_interest) ** self.total_months

        denominator = (1 + self.monthly_interest) ** self.total_months - 1

        return round(self.loan_amount * numerator / denominator, 2)

    def calculate(self):
        pass


fm = FixedMortgage(250_000, 4.25, 30, down_payment=0, points=2)
print(fm.monthly_payment())
