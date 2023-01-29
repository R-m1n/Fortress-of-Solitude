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

    def total_interest(self) -> float:
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

    def __init__(self, home_value: int | float, interest_rate: float, loan_term: int, down_payment: int | float = 0, fixed_points_combobox: int | float = 0) -> None:
        interest_rate = interest_rate - \
            (fixed_points_combobox * self.DISCOUNT_PER_POINT)

        super().__init__(home_value, interest_rate, loan_term, down_payment)

        self.fixed_points_combobox = fixed_points_combobox

        self.prepaid_interest = self.loan_amount * \
            (fixed_points_combobox / 100)

        self.point_cost = self.prepaid_interest / \
            fixed_points_combobox if fixed_points_combobox > 0 else 0

    def monthly_payment(self) -> float:
        numerator = \
            self.monthly_interest * \
            (1 + self.monthly_interest) ** self.total_months

        denominator = (1 + self.monthly_interest) ** self.total_months - 1

        return round(self.loan_amount * numerator / denominator, 2)

    def annual_payment(self) -> float:
        return round(self.monthly_payment() * self.MONTHS, 2)

    def total_payment(self) -> float:
        return round(self.monthly_payment() * self.total_months, 2)

    def calculate(self) -> str:
        log = ""
        log += f"Home Value:\t\t{float(self.home_value)}$\n\n"

        log += 47 * "="

        log += f"\n\nInterest Rate:\t\t{round(self.interest_rate * 100, 2)}%\nLoan Term:\t\t{self.loan_term} year(s)\nDown Payment:\t\t{self.down_payment}$\n"

        if self.fixed_points_combobox != 0:
            log += f"\nfixed_Points_combobox:\t\t\t{self.fixed_points_combobox}\nRate Discount:\t\t\t{(self.fixed_points_combobox * self.DISCOUNT_PER_POINT) * 100}%"
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

    def __init__(self, home_value: int | float, base_rate: float, loan_term: int, adj_fixed_period_combobox: int, adj_adjust_rate_combobox: float, down_payment: int | float = 0) -> None:

        super().__init__(home_value, base_rate, loan_term, down_payment)

        self.adj_fixed_period_combobox = adj_fixed_period_combobox

        self.adj_adjust_rate_combobox = adj_adjust_rate_combobox

    def monthly_payment(self) -> list[float]:
        fixed_mortgage = FixedMortgage(self.home_value, self.interest_rate,
                                       self.loan_term, self.down_payment)

        monthly_payments = [fixed_mortgage.monthly_payment()
                            for month in range(self.adj_fixed_period_combobox * self.MONTHS)]

        rate = self.interest_rate

        for month in range((self.loan_term - self.adj_fixed_period_combobox) * self.MONTHS):
            if month % self.MONTHS == 0:
                rate += self.adj_adjust_rate_combobox
                fixed_mortgage = FixedMortgage(self.home_value, rate,
                                               self.loan_term, self.down_payment)

            monthly_payments.append(fixed_mortgage.monthly_payment())

        return monthly_payments

    def annual_payment(self) -> list[float]:
        monthly_payments = self.monthly_payment()

        annual_payments = [round(monthly_payments[i] * self.MONTHS, 2)
                           for i in range(0, len(monthly_payments), self.MONTHS)]

        return annual_payments

    def total_payment(self) -> float:
        return round(functools.reduce(lambda a, b: a + b, self.monthly_payment()), 2)

    def calculate(self) -> str:
        log = ""
        log += f"Home Value:\t\t{float(self.home_value)}$\n\n"

        log += 47 * "="

        log += f"\n\nBase Rate:\t\t{round(self.interest_rate * 100, 2)}%\nLoan Term:\t\t{self.loan_term} year(s)\nDown Payment:\t\t{self.down_payment}$\n"

        log += f"\nFixed Period:\t\t {self.adj_fixed_period_combobox} year(s)\nAdjust Rate:\t\t {round(self.adj_adjust_rate_combobox * 100, 2)}%\nAdjust Interval:\tAnnual\n\n"

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


def fixed_calculate_callback() -> None:
    fixed_textbox.delete("0.0", "end")
    home_value = fixed_home_value_entry.get()

    if home_value == '':
        fixed_textbox.insert("0.0", "Please enter the Home Value!")
        return

    loan_term = fixed_loan_term_entry.get()

    if loan_term == '':
        fixed_textbox.insert("0.0", "Please enter the Loan Term!")
        return

    interest_rate = fixed_interest_rate_entry.get()

    if interest_rate == '':
        fixed_textbox.insert("0.0", "Please enter the Interest Rate!")
        return

    down_payment = fixed_down_payment_entry.get(
    ) if fixed_down_payment_entry.get() != '' else 0

    if fixed_unit_combobox.get() == "%":
        down_payment = float(home_value) * (float(down_payment) / 100)

    fixed_mortgage = FixedMortgage(float(home_value),
                                   float(interest_rate) / 100,
                                   int(loan_term),
                                   float(down_payment),
                                   int(fixed_points_combobox.get()))

    fixed_textbox.insert("0.0", fixed_mortgage.calculate())


def adjustable_calculate_callback() -> None:
    adj_textbox.delete("0.0", "end")
    home_value = adj_home_value_entry.get()

    if home_value == '':
        adj_textbox.insert("0.0", "Please enter the Home Value!")
        return

    loan_term = adj_loan_term_entry.get()

    if loan_term == '':
        adj_textbox.insert("0.0", "Please enter the Loan Term!")
        return

    base_rate = adj_interest_rate_entry.get()

    if base_rate == '':
        adj_textbox.insert("0.0", "Please enter the Interest Rate!")
        return

    down_payment = adj_down_payment_entry.get(
    ) if adj_down_payment_entry.get() != '' else 0

    if adj_unit_combobox.get() == "%":
        down_payment = float(home_value) * (float(down_payment) / 100)

    adjustable_mortgage = AdjustableMortgage(float(home_value),
                                             float(base_rate) / 100,
                                             int(loan_term),
                                             int(adj_fixed_period_combobox.get()),
                                             float(
                                                 adj_adjust_rate_combobox.get()) / 100,
                                             float(down_payment))

    adj_textbox.insert("0.0", adjustable_mortgage.calculate())


def fixed_clear_callback() -> None:
    fixed_textbox.delete("0.0", "end")
    fixed_home_value_entry.delete("0", "end")
    fixed_loan_term_entry.delete("0", "end")
    fixed_interest_rate_entry.delete("0", "end")
    fixed_down_payment_entry.delete("0", "end")
    fixed_unit_combobox.set("$")
    fixed_points_combobox.set("0")


def adjustable_clear_callback() -> None:
    adj_textbox.delete("0.0", "end")
    adj_home_value_entry.delete("0", "end")
    adj_loan_term_entry.delete("0", "end")
    adj_interest_rate_entry.delete("0", "end")
    adj_down_payment_entry.delete("0", "end")
    adj_unit_combobox.set("$")
    adj_adjust_rate_combobox.set("0.25")
    adj_fixed_period_combobox.set("0")


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
    fixed_frame_1 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), width=500, height=400, fg_color="transparent")
    fixed_frame_1.grid(row=0, column=0, pady=20, padx=60)

    fixed_textbox = customtkinter.CTkTextbox(
        fixed_frame_1, width=500, height=400, font=font)
    fixed_textbox.grid(row=0, column=0)

    fixed_frame_2 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), fg_color="transparent")
    fixed_frame_2.grid(row=1, column=0, padx=20)

    fixed_home_value_entry = customtkinter.CTkEntry(
        fixed_frame_2, placeholder_text="Home Value")
    fixed_home_value_entry.grid(row=0, column=0, pady=10, padx=5)

    fixed_home_value_label = customtkinter.CTkLabel(
        fixed_frame_2, text="$")
    fixed_home_value_label.grid(row=0, column=1, pady=10, padx=5)

    fixed_space_1 = customtkinter.CTkLabel(
        fixed_frame_2, text="", width=100)
    fixed_space_1.grid(row=0, column=2, pady=10, padx=5)

    fixed_loan_term_entry = customtkinter.CTkEntry(
        fixed_frame_2, placeholder_text="Loan Term")
    fixed_loan_term_entry.grid(row=0, column=3, pady=10, padx=5)

    fixed_loan_term_label = customtkinter.CTkLabel(
        fixed_frame_2, text="year(s)")
    fixed_loan_term_label.grid(row=0, column=4, pady=10, padx=5)

    fixed_interest_rate_entry = customtkinter.CTkEntry(
        fixed_frame_2, placeholder_text="Interest Rate")
    fixed_interest_rate_entry.grid(row=1, column=0, pady=10, padx=5)

    fixed_interest_rate_label = customtkinter.CTkLabel(
        fixed_frame_2, text="%")
    fixed_interest_rate_label.grid(row=1, column=1, pady=10, padx=5)

    fixed_space_2 = customtkinter.CTkLabel(
        fixed_frame_2, text="", width=100)
    fixed_space_2.grid(row=1, column=2, pady=10, padx=5)

    fixed_down_payment_entry = customtkinter.CTkEntry(
        fixed_frame_2, placeholder_text="Down Payment")
    fixed_down_payment_entry.grid(row=1, column=3, pady=10, padx=5)

    fixed_unit_combobox = customtkinter.CTkComboBox(
        fixed_frame_2, values=["$", "%"], width=50)
    fixed_unit_combobox.grid(row=1, column=4, pady=10, padx=5)
    fixed_unit_combobox.set("$")

    fixed_frame_3 = customtkinter.CTkFrame(
        tabview.tab("Fixed Mortgage"), fg_color="transparent")
    fixed_frame_3.grid(row=2, column=0, pady=20, padx=20)

    fixed_calculate_button = customtkinter.CTkButton(
        fixed_frame_3, command=fixed_calculate_callback, text="Calculate")
    fixed_calculate_button.grid(row=0, column=0, pady=10, padx=10)

    fixed_clear_button = customtkinter.CTkButton(
        fixed_frame_3, command=fixed_clear_callback, text="Clear")
    fixed_clear_button.grid(row=0, column=1, pady=10, padx=10)

    fixed_space_3 = customtkinter.CTkLabel(
        fixed_frame_3, text="", width=50)
    fixed_space_3.grid(row=0, column=2, pady=10, padx=5)

    fixed_points_label = customtkinter.CTkLabel(
        fixed_frame_3, text="Points:")
    fixed_points_label.grid(row=0, column=3, pady=10, padx=5)

    fixed_points_combobox = customtkinter.CTkComboBox(
        fixed_frame_3, values=[str(i) for i in range(11)], width=50)
    fixed_points_combobox.grid(row=0, column=4, pady=10, padx=10)
    fixed_points_combobox.set("0")

    # Adjustable Mortgage Tab
    adj_frame_1 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), width=500, height=400, fg_color="transparent")
    adj_frame_1.grid(row=0, column=0, pady=20, padx=60)

    adj_textbox = customtkinter.CTkTextbox(
        adj_frame_1, width=500, height=400, font=font)
    adj_textbox.grid(row=0, column=0)

    adj_frame_2 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), fg_color="transparent")
    adj_frame_2.grid(row=1, column=0, padx=20)

    adj_home_value_entry = customtkinter.CTkEntry(
        adj_frame_2, placeholder_text="Home Value")
    adj_home_value_entry.grid(row=0, column=0, pady=10, padx=5)

    adj_home_value_label = customtkinter.CTkLabel(
        adj_frame_2, text="$")
    adj_home_value_label.grid(row=0, column=1, pady=10, padx=5)

    adj_space_1 = customtkinter.CTkLabel(
        adj_frame_2, text="", width=100)
    adj_space_1.grid(row=0, column=2, pady=10, padx=5)

    adj_loan_term_entry = customtkinter.CTkEntry(
        adj_frame_2, placeholder_text="Loan Term")
    adj_loan_term_entry.grid(row=0, column=3, pady=10, padx=5)

    adj_loan_term_label = customtkinter.CTkLabel(
        adj_frame_2, text="year(s)")
    adj_loan_term_label.grid(row=0, column=4, pady=10, padx=5)

    adj_interest_rate_entry = customtkinter.CTkEntry(
        adj_frame_2, placeholder_text="Base Rate")
    adj_interest_rate_entry.grid(row=1, column=0, pady=10, padx=5)

    adj_interest_rate_label = customtkinter.CTkLabel(
        adj_frame_2, text="%")
    adj_interest_rate_label.grid(row=1, column=1, pady=10, padx=5)

    adj_space_2 = customtkinter.CTkLabel(
        adj_frame_2, text="", width=100)
    adj_space_2.grid(row=1, column=2, pady=10, padx=5)

    adj_down_payment_entry = customtkinter.CTkEntry(
        adj_frame_2, placeholder_text="Down Payment")
    adj_down_payment_entry.grid(row=1, column=3, pady=10, padx=5)

    adj_unit_combobox = customtkinter.CTkComboBox(
        adj_frame_2, values=["$", "%"], width=50)
    adj_unit_combobox.grid(row=1, column=4, pady=10, padx=5)
    adj_unit_combobox.set("$")

    adj_frame_3 = customtkinter.CTkFrame(
        tabview.tab("Adjustable Mortgage"), fg_color="transparent")
    adj_frame_3.grid(row=2, column=0, pady=10, padx=20)

    adj_frame_4 = customtkinter.CTkFrame(
        fixed_frame_3, fg_color="transparent")
    adj_frame_4.grid(row=0, column=0)

    adj_calculate_button = customtkinter.CTkButton(
        adj_frame_4, command=adjustable_calculate_callback, text="Calculate")
    adj_calculate_button.grid(row=0, column=0, pady=10, padx=10)

    adj_clear_button = customtkinter.CTkButton(
        adj_frame_4, command=adjustable_clear_callback, text="Clear")
    adj_clear_button.grid(row=1, column=0, pady=10, padx=10)

    adj_space_3 = customtkinter.CTkLabel(
        adj_frame_4, text="", width=170)
    adj_space_3.grid(row=0, column=2, pady=10, padx=5)

    adj_frame_5 = customtkinter.CTkFrame(
        adj_frame_3, fg_color="transparent")
    adj_frame_5.grid(row=0, column=1)

    adj_adjust_rate_label = customtkinter.CTkLabel(
        adj_frame_5, text="Adjust Rate:")
    adj_adjust_rate_label.grid(row=0, column=0, pady=10, padx=5)

    adj_adjust_rate_combobox = customtkinter.CTkComboBox(
        adj_frame_5, values=[str(i / 100) for i in range(25, 201, 25)], width=65)
    adj_adjust_rate_combobox.grid(row=0, column=1, padx=5)
    adj_adjust_rate_combobox.set("0.25")

    adj_fixed_period_label = customtkinter.CTkLabel(
        adj_frame_5, text="Fixed Period:")
    adj_fixed_period_label.grid(row=1, column=0, padx=5)

    adj_fixed_period_combobox = customtkinter.CTkComboBox(
        adj_frame_5, values=[str(i) for i in range(11)], width=65)
    adj_fixed_period_combobox.grid(row=1, column=1, padx=5)
    adj_fixed_period_combobox.set("0")

    app.mainloop()
