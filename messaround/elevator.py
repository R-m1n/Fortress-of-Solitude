

class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, route: dict, floor_count: int, start_floor: int = 1) -> None:
        self.route = route

        self.floor_count = self._set_floor_count(route, floor_count)

        self.current_floor = start_floor

        self.status = self._get_status(self.IDLE)

        self.log = f"""\nPassengers waiting on floors: {list(route.keys())}
                    \nCurrent floor: {self.current_floor}\n\n"""

        self.time = 0

    def elevate(self) -> None:

        while len(self.route) != 0:
            cabin = []

            self.current_floor = self._goto_closest()

            self.log += f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"

            cabin.append(self.current_floor)

            destination = self.route[self.current_floor]

            direction = self._get_direction(destination)

            self.status = self._get_status(direction)

            self.log += f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

            while len(cabin) != 0:
                self.current_floor += direction

                self.time += 1

                if self.current_floor in self.route \
                        and (self._get_direction(self.route[self.current_floor]) == direction
                             or self._get_direction(self.route[self.current_floor]) == self.IDLE):

                    self.log += f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"
                    cabin.append(self.current_floor)

                self.log += f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

                for passenger in cabin:
                    destination = self.route[passenger]

                    if self.current_floor == destination or destination == self.IDLE:
                        self.log += f"Removing passenger {passenger} at {self._ordinal(self.current_floor)} floor\n\n"

                        cabin.remove(passenger)
                        self.route.pop(passenger)

            self.status = self._get_status(self.IDLE)
            self.log += f"status: {self.status}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

        self.status = self._get_status(self.IDLE)
        self.log += f"\nTotal time: {elevator.time}s"

    def _goto_closest(self) -> int:
        self.log += "Going to the closest passenger...\n\n"

        if self.current_floor in self.route:
            return self.current_floor

        up_probe = self.current_floor
        down_probe = self.current_floor

        for floor_number in range(self.floor_count):
            up_probe += self.UP
            down_probe += self.DOWN

            self.time += 1

            if up_probe in self.route:
                return up_probe

            if down_probe in self.route:
                return down_probe

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

    def _get_status(self, status: int):
        return {1: "UP", 0: "IDLE", -1: "DOWN"}.get(status, "UNDER MAINTENANCE!")

    def _set_floor_count(self, route: dict, floor_count: int):
        if floor_count < max(route.values()):
            raise ValueError(
                f"Number of floors cannot be less than destination floor.")

        return floor_count


route = [(1, 5), (2, 4), (3, 1)]
route = dict(route)
elevator = Elevator(route, 5, 4)
elevator.elevate()
print(elevator.log)
