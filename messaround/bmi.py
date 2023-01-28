import customtkinter


def calculate_bmi() -> None:
    weight = 0 if weight_entry.get() == '' \
        else convert_weight(weight_combobox.get())(float(weight_entry.get()))

    height = 1 if height_entry.get() == '' \
        else convert_height(height_combobox.get())(float(height_entry.get()))

    return weight / pow(height, 2)


def convert_weight(unit: str) -> None:
    if unit == "g":
        return lambda weight: weight / 1000

    elif unit == "lbs":
        return lambda weight: weight / 2.205

    return lambda weight: weight


def convert_height(unit: str) -> None:
    if unit == "cm":
        return lambda height: height / 100

    elif unit == "inch":
        return lambda height: height / 39.37

    return lambda height: height


def evaluate(bmi: str | int | float) -> str:
    bmi = float(bmi)

    if bmi >= 30:
        return "Obese"

    elif 30 > bmi >= 25:
        return "Overweight"

    elif 25 > bmi >= 18.5:
        return "Normal"

    return "Underweight"


def create_toplevel() -> None:
    window = customtkinter.CTkToplevel()
    window.title('')

    bmi = "{:.1f}".format(calculate_bmi())
    bmi_label = customtkinter.CTkLabel(
        window, text=f"BMI:\t{bmi}", font=customtkinter.CTkFont(size=18))
    bmi_label.pack(side="top", fill="both", expand=True, padx=40, pady=10)

    evaluation_label = customtkinter.CTkLabel(
        window, text=f"{evaluate(bmi)}", font=customtkinter.CTkFont(size=18))
    evaluation_label.pack(side="top", fill="both",
                          expand=True, padx=40, pady=10)


def clear_entries() -> None:
    weight_entry.delete(0, len(weight_entry.get()))
    height_entry.delete(0, len(height_entry.get()))


def calculate_button_callback() -> None:
    create_toplevel()
    clear_entries()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry("360x200")
    app.title("BMI Calculator")

    frame_1 = customtkinter.CTkFrame(app)
    frame_1.grid(row=0, column=0, pady=20, padx=60)

    frame_2 = customtkinter.CTkFrame(app, fg_color="transparent")
    frame_2.grid(row=1, column=0, padx=60)

    weight_entry = customtkinter.CTkEntry(
        frame_1, placeholder_text="Weight")
    weight_entry.grid(row=0, column=0, pady=10, padx=10)

    weight_combobox = customtkinter.CTkComboBox(
        frame_1, width=60, values=["kg", "g", "lbs"])
    weight_combobox.grid(row=0, column=1, pady=10, padx=10)
    weight_combobox.set("kg")

    height_entry = customtkinter.CTkEntry(
        frame_1, placeholder_text="Height")
    height_entry.grid(row=1, column=0, pady=10, padx=10)

    height_combobox = customtkinter.CTkComboBox(
        frame_1, width=60, values=["m", "cm", "inch"])
    height_combobox.grid(row=1, column=1, pady=10, padx=10)
    height_combobox.set("m")

    calculate_button = customtkinter.CTkButton(
        frame_2, command=calculate_button_callback, text="Calculate")
    calculate_button.grid(row=0, column=0, pady=10, padx=10)

    app.mainloop()
