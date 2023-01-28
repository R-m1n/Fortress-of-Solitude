import customtkinter


class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, route: dict | list[tuple[int, int]]) -> None:
        self.route = self._set_route(route)

        self.floor_count = max(list(route.keys()) + list(route.values()))

        self.current_floor = 1

        self._set_status(self.IDLE)

        self.log = ""

        self.time = 0

    def elevate(self) -> None:

        self._log(f"""Passenger list:\n{list(self.route.keys())}
                    \nCurrent floor: {self.current_floor}\n\n""")

        while len(self.route) != 0:
            cabin = []

            self.current_floor = self._goto_closest()

            self._log(
                f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"
            )

            cabin.append(self.current_floor)

            destination = self.route.get(self.current_floor)

            direction = self._get_direction(destination)

            self._set_status(direction)

            self._log(
                f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"
            )

            self._deliver(cabin, direction)

            self._set_status(self.IDLE)

            self._log(
                f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"
            )

        self._log(
            f"\nTotal time: {self.time}s"
        )

    def _goto_closest(self) -> int:

        self._log(
            "Going to the closest passenger...\n\n"
        )

        if self.current_floor in self.route:
            return self.current_floor

        up_probe = down_probe = self.current_floor

        for floor_number in range(self.floor_count):
            up_probe += self.UP
            down_probe += self.DOWN

            self.time += 1

            if up_probe in self.route:
                return up_probe

            if down_probe in self.route:
                return down_probe

    def _deliver(self, cabin: list[int], direction: int) -> None:

        if direction == self.IDLE:
            self._stall(cabin[0])
            return

        while len(cabin) != 0:
            self.current_floor += direction

            self.time += 1

            is_passenger_waiting = self.current_floor in self.route

            if is_passenger_waiting:

                is_same_direction = self._get_direction(
                    self.route.get(self.current_floor)) == direction

                is_idle = self._get_direction(
                    self.route.get(self.current_floor)) == self.IDLE

                if is_same_direction or is_idle:

                    self._log(
                        f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"
                    )

                    cabin.append(self.current_floor)

            self._log(
                f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"
            )

            for passenger in cabin.copy():
                destination = self.route.get(passenger)

                if self.current_floor == destination or destination == self.IDLE:
                    self._stall(passenger)
                    cabin.remove(passenger)

    def _get_direction(self, destination: int) -> int:
        if self.current_floor == destination or destination == self.IDLE:
            return self.IDLE

        if self.current_floor > destination:
            return self.DOWN

        if self.current_floor < destination:
            return self.UP

    def _stall(self, passenger: int) -> None:

        self._log(
            f"Delivering passenger {passenger} at {self._ordinal(self.current_floor)} floor\n\n"
        )

        self.route.pop(passenger)

    def _ordinal(self, number: int) -> str:
        first_digit = number % 10
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(first_digit, "th")

        return f"{number}{suffix}"

    def _log(self, log: str) -> None:
        self.log += log

    def _set_route(self, route: dict | list[tuple[int, int]]) -> dict:
        if len(route) == 0:
            raise ValueError(
                "empty route."
            )

        return route if isinstance(route, dict) else dict(route)

    def _set_status(self, status: int):
        self.status = \
            {1: "UP", 0: "IDLE", -1: "DOWN"}.get(status, "UNDER MAINTENANCE!")


def add_button_callback() -> None:
    passenger = int(passenger_entry.get()) \
        if passenger_entry.get() != '' else 1

    destination = int(destination_entry.get()) \
        if destination_entry.get() != '' else 0

    if passenger in route:
        clear_entries()
        return

    if passenger != destination:
        route[passenger] = destination

    else:
        route[passenger] = 0

    record_textbox.insert("end", f"{passenger} -> {destination}, ")

    clear_entries()


def elevate_button_callback() -> None:
    log_textbox.delete("0.0", "end")

    try:
        elevator = Elevator(route)
        elevator.elevate()

    except ValueError as ve:
        log_textbox.insert("end", ve)

    log_textbox.insert("0.0", elevator.log)

    clear_route()


def clear_route() -> None:
    record_textbox.delete("0.0", "end")
    route.clear()


def clear_button_callback() -> None:
    log_textbox.delete("0.0", "end")
    clear_route()


def clear_entries() -> None:
    passenger_entry.delete(0, len(passenger_entry.get()))
    destination_entry.delete(0, len(destination_entry.get()))


if __name__ == "__main__":
    route = {}

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("dark-blue")

    app = customtkinter.CTk()
    app.geometry(f"{600}x{700}")
    app.title("Elevator Simulator")

    font = customtkinter.CTkFont(family="consolas", size=16)

    frame_1 = customtkinter.CTkFrame(
        app, width=500, height=400, fg_color="transparent")
    frame_1.grid(row=0, column=0, pady=20, padx=60)

    label = customtkinter.CTkLabel(frame_1,
                                   text="Event Logs",
                                   font=font,
                                   corner_radius=8)
    label.grid(row=0, column=0)

    log_textbox = customtkinter.CTkTextbox(
        frame_1, width=500, height=400, font=font)
    log_textbox.grid(row=1, column=0)

    record_textbox = customtkinter.CTkTextbox(
        frame_1, width=500, height=20, font=font)
    record_textbox.grid(row=2, column=0, pady=20)

    frame_2 = customtkinter.CTkFrame(app, fg_color="transparent")
    frame_2.grid(row=1, column=0, padx=20)

    passenger_entry = customtkinter.CTkEntry(
        frame_2, placeholder_text="Passenger")
    passenger_entry.grid(row=0, column=0, pady=10, padx=10)

    destination_entry = customtkinter.CTkEntry(
        frame_2, placeholder_text="Destination")
    destination_entry.grid(row=0, column=1, pady=10, padx=10)

    add_button = customtkinter.CTkButton(
        frame_2, command=add_button_callback, text="Add")
    add_button.grid(row=0, column=2, pady=10, padx=10)

    frame_3 = customtkinter.CTkFrame(app, fg_color="transparent")
    frame_3.grid(row=2, column=0, padx=40, pady=20)

    elevate_button = customtkinter.CTkButton(
        frame_3, command=elevate_button_callback, text="Elevate")
    elevate_button.grid(row=0, column=0, pady=10, padx=10)

    clear_button = customtkinter.CTkButton(
        frame_3, command=clear_button_callback, text="Clear")
    clear_button.grid(row=0, column=1, pady=10, padx=10)

    app.mainloop()
