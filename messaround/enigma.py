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


def settings_button_callback():
    def apply_button_callback():
        pass

    def cancel_button_callback():
        window.destroy()

    window = customtkinter.CTkToplevel()
    window.geometry(f"{420}x{700}")
    window.title("Settings")

    tab_frame = customtkinter.CTkFrame(
        window, width=380, height=600, fg_color="transparent")
    tab_frame.grid(row=0, column=0)

    tabview = customtkinter.CTkTabview(tab_frame, width=380, height=600)
    tabview.grid(row=0, column=0,
                 padx=(20, 0), pady=(20, 0), sticky="nsew")

    tabview.add("Rotor 1")
    tabview.add("Rotor 2")
    tabview.add("Rotor 3")
    tabview.add("Rotor 4")
    tabview.add("Rotor 5")
    tabview.add("Plugboard")

    tabview.set("Rotor 1")

    tabview.tab("Rotor 1").grid_columnconfigure(0, weight=1)
    tabview.tab("Rotor 2").grid_columnconfigure(0, weight=1)
    tabview.tab("Rotor 3").grid_columnconfigure(0, weight=1)
    tabview.tab("Rotor 4").grid_columnconfigure(0, weight=1)
    tabview.tab("Rotor 5").grid_columnconfigure(0, weight=1)
    tabview.tab("Plugboard").grid_columnconfigure(0, weight=1)

    rotor_1_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Rotor 1"), width=380, height=100, fg_color="transparent")
    rotor_1_tab_frame.grid(row=0, column=0, padx=10,
                           pady=30)

    rotor_1_tab_frame_1 = customtkinter.CTkFrame(rotor_1_tab_frame)
    rotor_1_tab_frame_1.grid(row=0, column=0, padx=20)

    rotor_1_tab_frame_2 = customtkinter.CTkFrame(rotor_1_tab_frame)
    rotor_1_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][0], width=50)
    a_1_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][1], width=50)
    b_1_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][2], width=50)
    c_1_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][3], width=50)
    d_1_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][4], width=50)
    e_1_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][5], width=50)
    f_1_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][6], width=50)
    g_1_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][7], width=50)
    h_1_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][8], width=50)
    i_1_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][9], width=50)
    j_1_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][10], width=50)
    k_1_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][11], width=50)
    l_1_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_1, placeholder_text=alts[0][12], width=50)
    m_1_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][13], width=50)
    n_1_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][14], width=50)
    o_1_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][15], width=50)
    p_1_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][16], width=50)
    q_1_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][17], width=50)
    r_1_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][18], width=50)
    s_1_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][19], width=50)
    t_1_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][20], width=50)
    u_1_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][21], width=50)
    v_1_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][22], width=50)
    w_1_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][23], width=50)
    x_1_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][24], width=50)
    y_1_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_1_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_1_entry = customtkinter.CTkEntry(
        rotor_1_tab_frame_2, placeholder_text=alts[0][25], width=50)
    z_1_entry.grid(row=13, column=2, pady=5, padx=10)

    rotor_2_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Rotor 2"), width=380, height=100, fg_color="transparent")
    rotor_2_tab_frame.grid(row=0, column=0, padx=10,
                           pady=30)

    rotor_2_tab_frame_1 = customtkinter.CTkFrame(rotor_2_tab_frame)
    rotor_2_tab_frame_1.grid(row=0, column=0, padx=20)

    rotor_2_tab_frame_2 = customtkinter.CTkFrame(rotor_2_tab_frame)
    rotor_2_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][0], width=50)
    a_2_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][1], width=50)
    b_2_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][2], width=50)
    c_2_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][3], width=50)
    d_2_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][4], width=50)
    e_2_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][5], width=50)
    f_2_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][6], width=50)
    g_2_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][7], width=50)
    h_2_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][8], width=50)
    i_2_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][9], width=50)
    j_2_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][10], width=50)
    k_2_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][11], width=50)
    l_2_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_1, placeholder_text=alts[1][12], width=50)
    m_2_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][13], width=50)
    n_2_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][14], width=50)
    o_2_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][15], width=50)
    p_2_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][16], width=50)
    q_2_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][17], width=50)
    r_2_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][18], width=50)
    s_2_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][19], width=50)
    t_2_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][20], width=50)
    u_2_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][21], width=50)
    v_2_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][22], width=50)
    w_2_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][23], width=50)
    x_2_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][24], width=50)
    y_2_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_2_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_2_entry = customtkinter.CTkEntry(
        rotor_2_tab_frame_2, placeholder_text=alts[1][25], width=50)
    z_2_entry.grid(row=13, column=2, pady=5, padx=10)

    rotor_3_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Rotor 3"), width=380, height=100, fg_color="transparent")
    rotor_3_tab_frame.grid(row=0, column=0, padx=10,
                           pady=30)

    rotor_3_tab_frame_1 = customtkinter.CTkFrame(rotor_3_tab_frame)
    rotor_3_tab_frame_1.grid(row=0, column=0, padx=20)

    rotor_3_tab_frame_2 = customtkinter.CTkFrame(rotor_3_tab_frame)
    rotor_3_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][0], width=50)
    a_3_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][1], width=50)
    b_3_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][2], width=50)
    c_3_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][3], width=50)
    d_3_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][4], width=50)
    e_3_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][5], width=50)
    f_3_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][6], width=50)
    g_3_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][7], width=50)
    h_3_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][8], width=50)
    i_3_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][9], width=50)
    j_3_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][10], width=50)
    k_3_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][11], width=50)
    l_3_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_1, placeholder_text=alts[2][12], width=50)
    m_3_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][13], width=50)
    n_3_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][14], width=50)
    o_3_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][15], width=50)
    p_3_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][16], width=50)
    q_3_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][17], width=50)
    r_3_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][18], width=50)
    s_3_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][19], width=50)
    t_3_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][20], width=50)
    u_3_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][21], width=50)
    v_3_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][22], width=50)
    w_3_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][23], width=50)
    x_3_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][24], width=50)
    y_3_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_3_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_3_entry = customtkinter.CTkEntry(
        rotor_3_tab_frame_2, placeholder_text=alts[2][25], width=50)
    z_3_entry.grid(row=13, column=2, pady=5, padx=10)

    rotor_4_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Rotor 4"), width=380, height=100, fg_color="transparent")
    rotor_4_tab_frame.grid(row=0, column=0, padx=10,
                           pady=30)

    rotor_4_tab_frame_1 = customtkinter.CTkFrame(rotor_4_tab_frame)
    rotor_4_tab_frame_1.grid(row=0, column=0, padx=20)

    rotor_4_tab_frame_2 = customtkinter.CTkFrame(rotor_4_tab_frame)
    rotor_4_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][0], width=50)
    a_4_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][1], width=50)
    b_4_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][2], width=50)
    c_4_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][3], width=50)
    d_4_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][4], width=50)
    e_4_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][5], width=50)
    f_4_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][6], width=50)
    g_4_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][7], width=50)
    h_4_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][8], width=50)
    i_4_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][9], width=50)
    j_4_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][10], width=50)
    k_4_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][11], width=50)
    l_4_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_1, placeholder_text=alts[3][12], width=50)
    m_4_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][13], width=50)
    n_4_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][14], width=50)
    o_4_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][15], width=50)
    p_4_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][16], width=50)
    q_4_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][17], width=50)
    r_4_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][18], width=50)
    s_4_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][19], width=50)
    t_4_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][20], width=50)
    u_4_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][21], width=50)
    v_4_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][22], width=50)
    w_4_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][23], width=50)
    x_4_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][24], width=50)
    y_4_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_4_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_4_entry = customtkinter.CTkEntry(
        rotor_4_tab_frame_2, placeholder_text=alts[3][25], width=50)
    z_4_entry.grid(row=13, column=2, pady=5, padx=10)

    rotor_5_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Rotor 5"), width=380, height=100, fg_color="transparent")
    rotor_5_tab_frame.grid(row=0, column=0, padx=10,
                           pady=30)

    rotor_5_tab_frame_1 = customtkinter.CTkFrame(rotor_5_tab_frame)
    rotor_5_tab_frame_1.grid(row=0, column=0, padx=20)

    rotor_5_tab_frame_2 = customtkinter.CTkFrame(rotor_5_tab_frame)
    rotor_5_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][0], width=50)
    a_5_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][1], width=50)
    b_5_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][2], width=50)
    c_5_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][3], width=50)
    d_5_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][4], width=50)
    e_5_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][5], width=50)
    f_5_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][6], width=50)
    g_5_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][7], width=50)
    h_5_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][8], width=50)
    i_5_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][9], width=50)
    j_5_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][10], width=50)
    k_5_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][11], width=50)
    l_5_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_1, placeholder_text=alts[4][12], width=50)
    m_5_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][13], width=50)
    n_5_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][14], width=50)
    o_5_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][15], width=50)
    p_5_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][16], width=50)
    q_5_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][17], width=50)
    r_5_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][18], width=50)
    s_5_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][19], width=50)
    t_5_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][20], width=50)
    u_5_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][21], width=50)
    v_5_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][22], width=50)
    w_5_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][23], width=50)
    x_5_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][24], width=50)
    y_5_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(rotor_5_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_5_entry = customtkinter.CTkEntry(
        rotor_5_tab_frame_2, placeholder_text=alts[4][25], width=50)
    z_5_entry.grid(row=13, column=2, pady=5, padx=10)

    plugboard_tab_frame = customtkinter.CTkFrame(
        tabview.tab("Plugboard"), width=380, height=100, fg_color="transparent")
    plugboard_tab_frame.grid(row=0, column=0, padx=10,
                             pady=30)

    plugboard_tab_frame_1 = customtkinter.CTkFrame(plugboard_tab_frame)
    plugboard_tab_frame_1.grid(row=0, column=0, padx=20)

    plugboard_tab_frame_2 = customtkinter.CTkFrame(plugboard_tab_frame)
    plugboard_tab_frame_2.grid(row=0, column=1, padx=20)

    a_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="a")
    a_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    a_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[0], width=50)
    a_plugboard_entry.grid(row=0, column=2, pady=5, padx=10)

    b_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="b")
    b_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    b_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[1], width=50)
    b_plugboard_entry.grid(row=1, column=2, pady=5, padx=10)

    c_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="c")
    c_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    c_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[2], width=50)
    c_plugboard_entry.grid(row=2, column=2, pady=5, padx=10)

    d_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="d")
    d_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    d_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[3], width=50)
    d_plugboard_entry.grid(row=3, column=2, pady=5, padx=10)

    e_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="e")
    e_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    e_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[4], width=50)
    e_plugboard_entry.grid(row=4, column=2, pady=5, padx=10)

    f_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="f")
    f_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    f_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[5], width=50)
    f_plugboard_entry.grid(row=5, column=2, pady=5, padx=10)

    g_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="g")
    g_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    g_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[6], width=50)
    g_plugboard_entry.grid(row=6, column=2, pady=5, padx=10)

    h_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="h")
    h_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    h_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[7], width=50)
    h_plugboard_entry.grid(row=7, column=2, pady=5, padx=10)

    i_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="i")
    i_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    i_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[8], width=50)
    i_plugboard_entry.grid(row=8, column=2, pady=5, padx=10)

    j_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="j")
    j_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    j_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[9], width=50)
    j_plugboard_entry.grid(row=9, column=2, pady=5, padx=10)

    k_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="k")
    k_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    k_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[10], width=50)
    k_plugboard_entry.grid(row=10, column=2, pady=5, padx=10)

    l_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="l")
    l_label.grid(row=11, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=11, column=1, pady=5, padx=10)

    l_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[11], width=50)
    l_plugboard_entry.grid(row=11, column=2, pady=5, padx=10)

    m_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="m")
    m_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_1, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    m_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_1, placeholder_text=plugboard_alt[12], width=50)
    m_plugboard_entry.grid(row=12, column=2, pady=5, padx=10)

    n_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="n")
    n_label.grid(row=0, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=0, column=1, pady=5, padx=10)

    n_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[13], width=50)
    n_plugboard_entry.grid(row=0, column=2, pady=5, padx=10)

    o_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="o")
    o_label.grid(row=1, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=1, column=1, pady=5, padx=10)

    o_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[14], width=50)
    o_plugboard_entry.grid(row=1, column=2, pady=5, padx=10)

    p_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="p")
    p_label.grid(row=2, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=2, column=1, pady=5, padx=10)

    p_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[15], width=50)
    p_plugboard_entry.grid(row=2, column=2, pady=5, padx=10)

    q_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="q")
    q_label.grid(row=3, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=3, column=1, pady=5, padx=10)

    q_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[16], width=50)
    q_plugboard_entry.grid(row=3, column=2, pady=5, padx=10)

    r_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="r")
    r_label.grid(row=4, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=4, column=1, pady=5, padx=10)

    r_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[17], width=50)
    r_plugboard_entry.grid(row=4, column=2, pady=5, padx=10)

    s_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="s")
    s_label.grid(row=5, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=5, column=1, pady=5, padx=10)

    s_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[18], width=50)
    s_plugboard_entry.grid(row=5, column=2, pady=5, padx=10)

    t_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="t")
    t_label.grid(row=6, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=6, column=1, pady=5, padx=10)

    t_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[19], width=50)
    t_plugboard_entry.grid(row=6, column=2, pady=5, padx=10)

    u_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="u")
    u_label.grid(row=7, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=7, column=1, pady=5, padx=10)

    u_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[20], width=50)
    u_plugboard_entry.grid(row=7, column=2, pady=5, padx=10)

    v_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="v")
    v_label.grid(row=8, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=8, column=1, pady=5, padx=10)

    v_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[21], width=50)
    v_plugboard_entry.grid(row=8, column=2, pady=5, padx=10)

    w_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="w")
    w_label.grid(row=9, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=9, column=1, pady=5, padx=10)

    w_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[22], width=50)
    w_plugboard_entry.grid(row=9, column=2, pady=5, padx=10)

    x_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="x")
    x_label.grid(row=10, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=10, column=1, pady=5, padx=10)

    x_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[23], width=50)
    x_plugboard_entry.grid(row=10, column=2, pady=5, padx=10)

    y_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="y")
    y_label.grid(row=12, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=12, column=1, pady=5, padx=10)

    y_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[24], width=50)
    y_plugboard_entry.grid(row=12, column=2, pady=5, padx=10)

    z_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="z")
    z_label.grid(row=13, column=0, pady=5, padx=10)

    arrow_label = customtkinter.CTkLabel(plugboard_tab_frame_2, text="->")
    arrow_label.grid(row=13, column=1, pady=5, padx=10)

    z_plugboard_entry = customtkinter.CTkEntry(
        plugboard_tab_frame_2, placeholder_text=plugboard_alt[25], width=50)
    z_plugboard_entry.grid(row=13, column=2, pady=5, padx=10)

    settings_buttons_frame = customtkinter.CTkFrame(
        window, width=380, height=100, fg_color="transparent")
    settings_buttons_frame.grid(row=1, column=0, padx=(20, 0), pady=(20, 0))

    apply_button = customtkinter.CTkButton(
        settings_buttons_frame, command=apply_button_callback, text="Apply")
    apply_button.grid(row=0, column=0, pady=10, padx=10)

    settings_space = customtkinter.CTkLabel(
        settings_buttons_frame, text="", width=20)
    settings_space.grid(row=0, column=1, pady=10, padx=5)

    cancel_button = customtkinter.CTkButton(
        settings_buttons_frame, command=cancel_button_callback, text="Cancel")
    cancel_button.grid(row=0, column=2, pady=10, padx=10)


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

    buttons_space = customtkinter.CTkLabel(
        buttons_frame, text="", width=210)
    buttons_space.grid(row=0, column=1, pady=10, padx=5)

    settings_button = customtkinter.CTkButton(
        buttons_frame, command=settings_button_callback, text="Settings")
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
