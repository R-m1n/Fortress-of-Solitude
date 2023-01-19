import customtkinter


def button_callback():
    create_toplevel()
    clear_entries()


def calculate_bmi():
    weight = 0 if entry_1.get() == '' \
        else convert_weight(combobox_1.get())(float(entry_1.get()))

    height = 1 if entry_2.get() == '' \
        else convert_height(combobox_2.get())(float(entry_2.get()))

    return weight / pow(height, 2)


def convert_weight(unit):
    if unit == "g":
        return lambda weight: weight / 1000

    elif unit == "lbs":
        return lambda weight: weight / 2.205

    return lambda weight: weight


def convert_height(unit):
    if unit == "cm":
        return lambda height: height / 100

    elif unit == "inch":
        return lambda height: height / 39.37

    return lambda height: height


def evaluate(bmi):
    bmi = float(bmi)

    if bmi >= 30:
        return "Obese"

    elif 30 > bmi >= 25:
        return "Overweight"

    elif 25 > bmi >= 18.5:
        return "Normal"

    return "Underweight"


def create_toplevel():
    window = customtkinter.CTkToplevel()
    window.title('')

    bmi = "{:.1f}".format(calculate_bmi())
    label_1 = customtkinter.CTkLabel(
        window, text=f"BMI:\t{bmi}", font=customtkinter.CTkFont(size=18))
    label_1.pack(side="top", fill="both", expand=True, padx=40, pady=10)

    label_2 = customtkinter.CTkLabel(
        window, text=f"{evaluate(bmi)}", font=customtkinter.CTkFont(size=18))
    label_2.pack(side="top", fill="both", expand=True, padx=40, pady=10)


def clear_entries():
    entry_1.delete(0, len(entry_1.get()))
    entry_2.delete(0, len(entry_2.get()))


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry("360x200")
    app.title("BMI Calculator")

    frame_1 = customtkinter.CTkFrame(master=app)
    frame_1.grid(row=0, column=0, pady=20, padx=60)

    frame_2 = customtkinter.CTkFrame(master=app, fg_color="transparent")
    frame_2.grid(row=1, column=0, padx=60)

    entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Weight")
    entry_1.grid(row=0, column=0, pady=10, padx=10)

    combobox_1 = customtkinter.CTkComboBox(
        frame_1, width=60, values=["kg", "g", "lbs"])
    combobox_1.grid(row=0, column=1, pady=10, padx=10)
    combobox_1.set("kg")

    entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Height")
    entry_2.grid(row=1, column=0, pady=10, padx=10)

    combobox_2 = customtkinter.CTkComboBox(
        frame_1, width=60, values=["m", "cm", "inch"])
    combobox_2.grid(row=1, column=1, pady=10, padx=10)
    combobox_2.set("m")

    button_1 = customtkinter.CTkButton(
        master=frame_2, command=button_callback, text="Calculate")
    button_1.grid(row=0, column=0, pady=10, padx=10)

    app.mainloop()
