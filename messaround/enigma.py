import string
import random
import customtkinter
import copy


class Rotor:
    ALPHABET_SIZE = len(string.ascii_lowercase)

    def __init__(self, alternative: str, rotation: int = 0) -> None:
        self.alphabet = list(string.ascii_lowercase)
        self.alternative = list(alternative)

        self.rotations = 0

        self.rotate(rotation)

    def rotate(self, rotation: int = 1):
        for n in range(rotation):
            self._count_rotation()
            self.alternative.append(self.alternative.pop(0))

        self.combination = dict(zip(self.alphabet, self.alternative))

    def get(self, letter: str, reverse: bool = False):
        return self.combination.get(letter, "#") if not reverse else dict(zip(self.alternative, self.alphabet)).get(letter, "#")

    def _count_rotation(self):
        self.rotations += 1
        self.rotations %= self.ALPHABET_SIZE


class Plugboard:
    def __init__(self, alternative: str) -> None:
        self.alphabet = list(string.ascii_lowercase)
        self.alternative = list(alternative)

        self.combination = dict(zip(self.alphabet, self.alternative))
        self.reverse_combination = dict(zip(self.alternative, self.alphabet))

    def get(self, letter: str, reverse: bool = False):
        return self.combination.get(letter, "#") if not reverse else self.reverse_combination.get(letter, "#")


class Enigma:
    def __init__(self, rotor_1: Rotor, rotor_2: Rotor, rotor_3: Rotor, plugboard: Plugboard) -> None:
        self.rotor_1 = rotor_1
        self.rotor_2 = rotor_2
        self.rotor_3 = rotor_3

        self.plugboard = plugboard

        self.reflector = dict(zip(list(string.ascii_lowercase),
                                  list(string.ascii_lowercase[::-1])))

    def convert(self, text: str):
        cipher = ""
        for letter in text:
            cipher += self._encode(letter)
            self._rotate()

        return cipher

    def _encode(self, letter: str):
        letter = letter.lower()

        encoded = self.plugboard.get(letter)

        encoded = self.rotor_1.get(encoded)
        encoded = self.rotor_2.get(encoded)
        encoded = self.rotor_3.get(encoded)

        encoded = self.reflector.get(encoded)

        encoded = self.rotor_3.get(encoded, reverse=True)
        encoded = self.rotor_2.get(encoded, reverse=True)
        encoded = self.rotor_1.get(encoded, reverse=True)

        encoded = self.plugboard.get(encoded, reverse=True)

        return encoded

    def _rotate(self):
        self.rotor_1.rotate()

        if self.rotor_1.rotations == 0:
            self.rotor_2.rotate()

            if self.rotor_2.rotations == 0:
                self.rotor_3.rotate()


def convert_button_callback():
    alt_1 = alts[int(rotor_1_combobox.get()) - 1]
    rot_1 = rotor_1_entry.get() if rotor_1_entry.get() != '' else 0

    rotor_1 = Rotor(alt_1, int(rot_1))

    alt_2 = alts[int(rotor_2_combobox.get()) - 1]
    rot_2 = rotor_2_entry.get() if rotor_2_entry.get() != '' else 0

    rotor_2 = Rotor(alt_2, int(rot_2))

    alt_3 = alts[int(rotor_3_combobox.get()) - 1]
    rot_3 = rotor_3_entry.get() if rotor_3_entry.get() != '' else 0

    rotor_3 = Rotor(alt_3, int(rot_3))

    plugboard = Plugboard(plugboard_alt)

    enigma = Enigma(rotor_1, rotor_2, rotor_3, plugboard)

    text = output_textbox.get("0.0", "end").strip()

    output_textbox.delete("0.0", "end")
    output_textbox.insert("0.0", enigma.convert(text))


if __name__ == "__main__":
    alts = [
        "eyozmukxsacwrhltjvnibfpgqd",
        "cjnaovgfyuebrqixwksdtpmzlh",
        "wnkfoeuqjmdbzpcxigyratlhvs",
        "hprsdkobvemwgtqfxyjznuliac",
        "awdtqrbygkejnolpismuzcfhvx",
    ]

    plugboard_alt = "lpmfhrobsuzqjkvcnxweadtiyg"

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry(f"{665}x{740}")
    app.title("Enigma")

    text_font = customtkinter.CTkFont(family="consolas", size=16)
    label_font = customtkinter.CTkFont(family="consolas", size=24)
    entry_font = customtkinter.CTkFont(size=10)

    buttons_frame = customtkinter.CTkFrame(
        app, width=600, height=200, fg_color="transparent")
    buttons_frame.grid(row=0, column=0, pady=20, padx=60)

    convert_button = customtkinter.CTkButton(
        buttons_frame, command=convert_button_callback, text="Convert")
    convert_button.grid(row=0, column=0, pady=10, padx=10)

    space_1 = customtkinter.CTkLabel(
        buttons_frame, text="", width=210)
    space_1.grid(row=0, column=1, pady=10, padx=5)

    settings_button = customtkinter.CTkButton(
        buttons_frame, command=lambda i: i, text="Settings")
    settings_button.grid(row=0, column=2, pady=10, padx=10)

    output_frame = customtkinter.CTkFrame(
        app, width=520, height=400, fg_color="transparent")
    output_frame.grid(row=1, column=0, pady=20, padx=60)

    output_textbox = customtkinter.CTkTextbox(
        output_frame, width=520, height=400, font=text_font)
    output_textbox.grid(row=0, column=0)

    rotors_frame = customtkinter.CTkFrame(
        app, width=520, height=200, fg_color="transparent")
    rotors_frame.grid(row=2, column=0, pady=20, padx=60)

    rotor_1_frame = customtkinter.CTkFrame(
        rotors_frame, width=520, height=200)
    rotor_1_frame.grid(row=0, column=0, pady=20, padx=60)

    rotor_1_label = customtkinter.CTkLabel(
        rotor_1_frame, text="I", font=label_font)
    rotor_1_label.grid(row=0, column=0, pady=10, padx=5)

    rotor_1_combobox = customtkinter.CTkComboBox(
        rotor_1_frame, values=[str(i) for i in range(1, 6)], width=50)
    rotor_1_combobox.grid(row=1, column=0, pady=10, padx=5)
    rotor_1_combobox.set("1")

    rotor_1_entry = customtkinter.CTkEntry(
        rotor_1_frame, placeholder_text="rotation", width=50, font=entry_font)
    rotor_1_entry.grid(row=2, column=0, pady=10, padx=5)

    rotor_2_frame = customtkinter.CTkFrame(
        rotors_frame, width=520, height=200)
    rotor_2_frame.grid(row=0, column=1, pady=20, padx=60)

    rotor_2_label = customtkinter.CTkLabel(
        rotor_2_frame, text="II", font=label_font)
    rotor_2_label.grid(row=0, column=0, pady=10, padx=5)

    rotor_2_combobox = customtkinter.CTkComboBox(
        rotor_2_frame, values=[str(i) for i in range(1, 6)], width=50)
    rotor_2_combobox.grid(row=1, column=0, pady=10, padx=5)
    rotor_2_combobox.set("2")

    rotor_2_entry = customtkinter.CTkEntry(
        rotor_2_frame, placeholder_text="rotation", width=50, font=entry_font)
    rotor_2_entry.grid(row=2, column=0, pady=10, padx=5)

    rotor_3_frame = customtkinter.CTkFrame(
        rotors_frame, width=520, height=200)
    rotor_3_frame.grid(row=0, column=2, pady=20, padx=60)

    rotor_3_label = customtkinter.CTkLabel(
        rotor_3_frame, text="III", font=label_font)
    rotor_3_label.grid(row=0, column=0, pady=10, padx=5)

    rotor_3_combobox = customtkinter.CTkComboBox(
        rotor_3_frame, values=[str(i) for i in range(1, 6)], width=50)
    rotor_3_combobox.grid(row=1, column=0, pady=10, padx=5)
    rotor_3_combobox.set("3")

    rotor_3_entry = customtkinter.CTkEntry(
        rotor_3_frame, placeholder_text="rotation", width=50, font=entry_font)
    rotor_3_entry.grid(row=2, column=0, pady=10, padx=5)

    app.mainloop()
