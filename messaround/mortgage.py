import functools
import customtkinter
from abc import ABC, abstractmethod


class Mortgage(ABC):
    MONTHS = 12

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0) -> None:
        self.home_value = home_value

        self.down_payment = down_payment

        self.interest_rate = interest_rate

        self.loan_term = loan_term

        self.loan_amount = self.home_value - self.down_payment

        self.monthly_interest = self.interest_rate / self.MONTHS

        self.total_months = self.loan_term * self.MONTHS

    def total_interest(self):
        return round(self.total_payment() - self.loan_amount, 2)

    @abstractmethod
    def monthly_payment(self):
        pass

    @abstractmethod
    def annual_payment(self):
        pass

    @abstractmethod
    def total_payment(self):
        pass

    @abstractmethod
    def calculate(self):
        pass


class FixedMortgage(Mortgage):
    DISCOUNT_PER_POINT = .0025

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0, points: int | float = 0) -> None:
        interest_rate = interest_rate - (points * self.DISCOUNT_PER_POINT)

        super().__init__(home_value, interest_rate, loan_term, down_payment)

        self.points = points

        self.prepaid_interest = self.loan_amount * (points / 100)

        self.point_cost = self.prepaid_interest / points if points > 0 else 0

    def monthly_payment(self):
        numerator = \
            self.monthly_interest * \
            (1 + self.monthly_interest) ** self.total_months

        denominator = (1 + self.monthly_interest) ** self.total_months - 1

        return round(self.loan_amount * numerator / denominator, 2)

    def annual_payment(self):
        return round(self.monthly_payment() * self.MONTHS, 2)

    def total_payment(self):
        return round(self.monthly_payment() * self.total_months, 2)

    def calculate(self):
        log = ""
        log += f"Home Value:\t\t{float(self.home_value)}$\n\n"
        log += 47 * "="
        log += f"\n\nInterest Rate:\t\t{round(self.interest_rate * 100, 2)}%\nLoan Term:\t\t{self.loan_term} year(s)\nDown Payment:\t\t{self.down_payment}$\n"

        if self.points != 0:
            log += f"\nPoints:\t\t\t{self.points}\nRate Discount:\t\t\t{(self.points * self.DISCOUNT_PER_POINT) * 100}%"
            log += f"\nPre-Paid Interest:\t\t\t{self.prepaid_interest}$\nPoint Cost:\t\t\t{self.point_cost}$\n\n"

        log += 47 * "-"
        log += f"\n\nMonthly Payment:\t{self.monthly_payment()}$\n"
        log += f"Annual Payment:\t\t{self.annual_payment()}$\n\n"
        log += f"Loan Amount:\t\t {float(self.loan_amount)}$\n"
        log += f"Total Interest:\t\t{self.total_interest()}$\n"
        log += 26 * "-"
        log += f"\nTotal Payment:\t\t {self.total_payment()}$\n\n"
        log += 47 * "="

        return log


class AdjustableMortgage(Mortgage):

    def __init__(self, home_value: int | float, base_rate: float, loan_term: int, fixed_period: int, adjust_rate: float, down_payment: int | float = 0) -> None:

        super().__init__(home_value, base_rate, loan_term, down_payment)

        self.fixed_period = fixed_period

        self.adjust_rate = adjust_rate

    def monthly_payment(self):
        fixed_mortgage = FixedMortgage(self.home_value, self.interest_rate,
                                       self.loan_term, self.down_payment)

        monthly_payments = [fixed_mortgage.monthly_payment()
                            for month in range(self.fixed_period * self.MONTHS)]

        rate = self.interest_rate

        for month in range((self.loan_term - self.fixed_period) * self.MONTHS):
            if month % self.MONTHS == 0:
                rate += self.adjust_rate
                fixed_mortgage = FixedMortgage(self.home_value, rate,
                                               self.loan_term, self.down_payment)

            monthly_payments.append(fixed_mortgage.monthly_payment())

        return monthly_payments

    def annual_payment(self):
        monthly_payments = self.monthly_payment()

        annual_payments = [round(monthly_payments[i] * self.MONTHS, 2)
                           for i in range(0, len(monthly_payments), self.MONTHS)]

        return annual_payments

    def total_payment(self):
        return round(functools.reduce(lambda a, b: a + b, self.monthly_payment()), 2)

    def calculate(self):
        log = ""
        log += f"Home Value:\t\t{float(self.home_value)}$\n\n"
        log += 47 * "="
        log += f"\n\nBase Rate:\t\t{round(self.interest_rate * 100, 2)}%\nLoan Term:\t\t{self.loan_term} year(s)\nDown Payment:\t\t{self.down_payment}$\n"

        log += f"\nFixed Period:\t\t {self.fixed_period} year(s)\nAdjust Rate:\t\t {round(self.adjust_rate * 100, 2)}%\nAdjust Interval:\tAnnual\n\n"

        log += 47 * "-"

        log += f"\n\nMonthly Payments:\n"
        monthly_payment = self.monthly_payment()
        for month in range(1, self.loan_term * self.MONTHS, self.MONTHS):
            log += f"{month}-{month + (self.MONTHS - 1)}\t\t{monthly_payment[month]}$\n"

        log += "\n"

        log += f"Annual Payments:\n"
        annual_payment = self.annual_payment()
        for year in range(1, self.loan_term + 1):
            log += f"{year}\t\t{annual_payment[year - 1]}$\n"

        log += "\n"

        log += f"Loan Amount:\t\t {float(self.loan_amount)}$\n"
        log += f"Total Interest:\t\t{self.total_interest()}$\n"
        log += 34 * "-"
        log += f"\nTotal Payment:\t\t {self.total_payment()}$\n\n"
        log += 47 * "="

        return log


def fixed_calculate_callback():
    textbox_1.delete("0.0", "end")
    home_value = home_value_1.get()

    if home_value == '':
        textbox_1.insert("0.0", "Please enter the Home Value!")
        return

    loan_term = loan_term_1.get()

    if loan_term == '':
        textbox_1.insert("0.0", "Please enter the Loan Term!")
        return

    interest_rate = interest_rate_1.get()

    if interest_rate == '':
        textbox_1.insert("0.0", "Please enter the Interest Rate!")
        return

    down_payment = down_payment_1.get() if down_payment_1.get() != '' else 0

    if unit_1.get() == "%":
        down_payment = float(home_value) * (float(down_payment) / 100)

    fixed_mortgage = FixedMortgage(float(home_value),
                                   float(interest_rate) / 100,
                                   int(loan_term),
                                   float(down_payment),
                                   int(points.get()))

    textbox_1.insert("0.0", fixed_mortgage.calculate())


def adjustable_calculate_callback():
    textbox_2.delete("0.0", "end")
    home_value = home_value_2.get()

    if home_value == '':
        textbox_2.insert("0.0", "Please enter the Home Value!")
        return

    loan_term = loan_term_2.get()

    if loan_term == '':
        textbox_2.insert("0.0", "Please enter the Loan Term!")
        return

    base_rate = interest_rate_2.get()

    if base_rate == '':
        textbox_2.insert("0.0", "Please enter the Interest Rate!")
        return

    down_payment = down_payment_2.get() if down_payment_2.get() != '' else 0

    if unit_2.get() == "%":
        down_payment = float(home_value) * (float(down_payment) / 100)

    adjustable_mortgage = AdjustableMortgage(float(home_value),
                                             float(base_rate) / 100,
                                             int(loan_term),
                                             int(fixed_period.get()),
                                             float(adjust_rate.get()) / 100,
                                             float(down_payment))

    textbox_2.insert("0.0", adjustable_mortgage.calculate())


def fixed_clear_callback():
    textbox_1.delete("0.0", "end")
    home_value_1.delete("0", "end")
    loan_term_1.delete("0", "end")
    interest_rate_1.delete("0", "end")
    down_payment_1.delete("0", "end")
    unit_1.set("$")
    points.set("0")


def adjustable_clear_callback():
    textbox_2.delete("0.0", "end")
    home_value_2.delete("0", "end")
    loan_term_2.delete("0", "end")
    interest_rate_2.delete("0", "end")
    down_payment_2.delete("0", "end")
    unit_2.set("$")
    adjust_rate.set("0.25")
    fixed_period.set("0")


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry(f"{665}x{740}")
    app.title("Mortgage Calculator")

    font = customtkinter.CTkFont(family="consolas", size=16)

    tabview = customtkinter.CTkTabview(app, width=565, height=665)
    tabview.grid(row=0, column=2,
                 padx=(20, 0), pady=(20, 0), sticky="nsew")

    tabview.add("Fixed Mortgage")
    tabview.add("Adjustable Mortgage")
    tabview.set("Fixed Mortgage")

    tabview.tab("Fixed Mortgage").grid_columnconfigure(0, weight=1)
    tabview.tab("Adjustable Mortgage").grid_columnconfigure(0, weight=1)

    # Fixed Mortgage Tab
    frame_1 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), width=500, height=400, fg_color="transparent")
    frame_1.grid(row=0, column=0, pady=20, padx=60)

    textbox_1 = customtkinter.CTkTextbox(
        frame_1, width=500, height=400, font=font)
    textbox_1.grid(row=0, column=0)

    frame_2 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), fg_color="transparent")
    frame_2.grid(row=1, column=0, padx=20)

    home_value_1 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Home Value")
    home_value_1.grid(row=0, column=0, pady=10, padx=5)

    label_1 = customtkinter.CTkLabel(
        frame_2, text="$")
    label_1.grid(row=0, column=1, pady=10, padx=5)

    space_1 = customtkinter.CTkLabel(
        frame_2, text="", width=100)
    space_1.grid(row=0, column=2, pady=10, padx=5)

    loan_term_1 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Loan Term")
    loan_term_1.grid(row=0, column=3, pady=10, padx=5)

    label_2 = customtkinter.CTkLabel(
        frame_2, text="year(s)")
    label_2.grid(row=0, column=4, pady=10, padx=5)

    interest_rate_1 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Interest Rate")
    interest_rate_1.grid(row=1, column=0, pady=10, padx=5)

    label_3 = customtkinter.CTkLabel(
        frame_2, text="%")
    label_3.grid(row=1, column=1, pady=10, padx=5)

    space_2 = customtkinter.CTkLabel(
        frame_2, text="", width=100)
    space_2.grid(row=1, column=2, pady=10, padx=5)

    down_payment_1 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Down Payment")
    down_payment_1.grid(row=1, column=3, pady=10, padx=5)

    unit_1 = customtkinter.CTkComboBox(
        frame_2, values=["$", "%"], width=50)
    unit_1.grid(row=1, column=4, pady=10, padx=5)
    unit_1.set("$")

    frame_3 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), fg_color="transparent")
    frame_3.grid(row=2, column=0, pady=20, padx=20)

    calculate_1 = customtkinter.CTkButton(
        frame_3, command=fixed_calculate_callback, text="Calculate")
    calculate_1.grid(row=0, column=0, pady=10, padx=10)

    clear_1 = customtkinter.CTkButton(
        frame_3, command=fixed_clear_callback, text="Clear")
    clear_1.grid(row=0, column=1, pady=10, padx=10)

    space_3 = customtkinter.CTkLabel(
        frame_3, text="", width=50)
    space_3.grid(row=0, column=2, pady=10, padx=5)

    label_4 = customtkinter.CTkLabel(
        frame_3, text="Points:")
    label_4.grid(row=0, column=3, pady=10, padx=5)

    points = customtkinter.CTkComboBox(
        frame_3, values=[str(i) for i in range(11)], width=50)
    points.grid(row=0, column=4, pady=10, padx=10)
    points.set("0")

    # Adjustable Mortgage Tab
    frame_1 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), width=500, height=400, fg_color="transparent")
    frame_1.grid(row=0, column=0, pady=20, padx=60)

    textbox_2 = customtkinter.CTkTextbox(
        frame_1, width=500, height=400, font=font)
    textbox_2.grid(row=0, column=0)

    frame_2 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), fg_color="transparent")
    frame_2.grid(row=1, column=0, padx=20)

    home_value_2 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Home Value")
    home_value_2.grid(row=0, column=0, pady=10, padx=5)

    label_1 = customtkinter.CTkLabel(
        frame_2, text="$")
    label_1.grid(row=0, column=1, pady=10, padx=5)

    space_1 = customtkinter.CTkLabel(
        frame_2, text="", width=100)
    space_1.grid(row=0, column=2, pady=10, padx=5)

    loan_term_2 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Loan Term")
    loan_term_2.grid(row=0, column=3, pady=10, padx=5)

    label_2 = customtkinter.CTkLabel(
        frame_2, text="year(s)")
    label_2.grid(row=0, column=4, pady=10, padx=5)

    interest_rate_2 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Base Rate")
    interest_rate_2.grid(row=1, column=0, pady=10, padx=5)

    label_3 = customtkinter.CTkLabel(
        frame_2, text="%")
    label_3.grid(row=1, column=1, pady=10, padx=5)

    space_2 = customtkinter.CTkLabel(
        frame_2, text="", width=100)
    space_2.grid(row=1, column=2, pady=10, padx=5)

    down_payment_2 = customtkinter.CTkEntry(
        frame_2, placeholder_text="Down Payment")
    down_payment_2.grid(row=1, column=3, pady=10, padx=5)

    unit_2 = customtkinter.CTkComboBox(
        frame_2, values=["$", "%"], width=50)
    unit_2.grid(row=1, column=4, pady=10, padx=5)
    unit_2.set("$")

    frame_3 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), fg_color="transparent")
    frame_3.grid(row=2, column=0, pady=10, padx=20)

    frame_4 = customtkinter.CTkFrame(
        frame_3, fg_color="transparent")
    frame_4.grid(row=0, column=0)

    calculate_2 = customtkinter.CTkButton(
        frame_4, command=adjustable_calculate_callback, text="Calculate")
    calculate_2.grid(row=0, column=0, pady=10, padx=10)

    clear_2 = customtkinter.CTkButton(
        frame_4, command=adjustable_clear_callback, text="Clear")
    clear_2.grid(row=1, column=0, pady=10, padx=10)

    space_3 = customtkinter.CTkLabel(
        frame_4, text="", width=170)
    space_3.grid(row=0, column=2, pady=10, padx=5)

    frame_5 = customtkinter.CTkFrame(
        frame_3, fg_color="transparent")
    frame_5.grid(row=0, column=1)

    label_4 = customtkinter.CTkLabel(
        frame_5, text="Adjust Rate:")
    label_4.grid(row=0, column=0, pady=10, padx=5)

    adjust_rate = customtkinter.CTkComboBox(
        frame_5, values=[str(i / 100) for i in range(25, 201, 25)], width=65)
    adjust_rate.grid(row=0, column=1, padx=5)
    adjust_rate.set("0.25")

    label_6 = customtkinter.CTkLabel(
        frame_5, text="Fixed Period:")
    label_6.grid(row=1, column=0, padx=5)

    fixed_period = customtkinter.CTkComboBox(
        frame_5, values=[str(i) for i in range(11)], width=65)
    fixed_period.grid(row=1, column=1, padx=5)
    fixed_period.set("0")

    app.mainloop()
