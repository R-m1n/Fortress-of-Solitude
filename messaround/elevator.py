

class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    DEFAULT_FLOOR = 1

    def __init__(self, route: dict | list[tuple], floor_count: int, start_floor: int = DEFAULT_FLOOR) -> None:
        self.route = route if isinstance(route, dict) else dict(route)

        self.floor_count = self._set_floor_count(route, floor_count)

        self.current_floor = self._set_start_floor(start_floor)

        self._set_status(self.IDLE)

        self.log = f"""\nPassengers waiting on floors: {list(route.keys())}
                    \nCurrent floor: {self.current_floor}\n\n"""

        self.time = 0

    def elevate(self) -> None:

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
            f"\nTotal time: {elevator.time}s"
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

    def _deliver(self, cabin: list, direction: int) -> None:
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

            for passenger in cabin:
                destination = self.route.get(passenger)

                if self.current_floor == destination or destination == self.IDLE:

                    self._log(
                        f"Removing passenger {passenger} at {self._ordinal(self.current_floor)} floor\n\n"
                    )

                    cabin.remove(passenger)
                    self.route.pop(passenger)

    def _get_direction(self, destination: int) -> int:

        if self.current_floor == destination or destination == self.IDLE:
            return self.IDLE

        if self.current_floor > destination:
            return self.DOWN

        if self.current_floor < destination:
            return self.UP

    def _ordinal(self, number: int) -> str:
        first_digit = number % 10
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(first_digit, "th")

        return f"{number}{suffix}"

    def _log(self, log: str) -> None:
        self.log += log

    def _set_status(self, status: int):
        self.status = {1: "UP", 0: "IDLE", -
                       1: "DOWN"}.get(status, "UNDER MAINTENANCE!")

    def _set_start_floor(self, start_floor: int) -> int:
        if start_floor < 1:
            raise ValueError(
                "start floor cannot be less than 1."
            )

        if isinstance(start_floor, int):
            return start_floor

        raise ValueError(
            f"start floor should be an integer not {type(start_floor)}."
        )

    def _set_floor_count(self, route: dict, floor_count: int) -> int:
        if floor_count < max(route.values()):
            raise ValueError(
                "destination floor cannot be greater than number of floors."
            )

        if isinstance(floor_count, int):
            return floor_count

        raise ValueError(
            f"number of floors should be an integer not {type(floor_count)}."
        )


route = {4: 5, 2: 4, 3: 1}
elevator = Elevator(route, 5)
elevator.elevate()
print(elevator.log)
