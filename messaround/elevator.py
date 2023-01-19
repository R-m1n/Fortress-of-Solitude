

class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, route: dict, start_floor: int = 1) -> None:
        self.route = route

        self.floor_count = max(route.values())

        self.current_floor = start_floor

        self.status = self.IDLE

        self.log = f"""\nPassengers waiting on floors: {list(route.keys())}
                    \nCurrent floor: {self.current_floor}\n\n"""

        self.movement = 0

    def elevate(self) -> None:

        if len(self.route) == 0:
            self.log += f"\nTotal movements: {elevator.movement}"
            return

        cabin = []

        self.current_floor = self._goto_closest()

        self.log += f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"
        cabin.append(self.current_floor)

        destination = self.route[self.current_floor]

        self.status = self._get_status(destination)

        self.log += f"status: {self._status_str(self.status)}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

        while len(cabin) != 0:
            self.current_floor += self.status

            self.movement += 1

            if self.current_floor in self.route \
                    and (self._get_status(self.route[self.current_floor]) == self.status
                         or self._get_status(self.route[self.current_floor]) == self.IDLE):

                self.log += f"Picking up passenger {self.current_floor} at {self._ordinal(self.current_floor)} floor\n\n"
                cabin.append(self.current_floor)

            self.log += f"status: {self._status_str(self.status)}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

            for passenger in cabin:
                destination = self.route[passenger]

                if self.current_floor == destination or destination == self.IDLE:
                    self.log += f"Removing passenger {passenger} at {self._ordinal(self.current_floor)} floor\n\n"

                    cabin.remove(passenger)
                    self.route.pop(passenger)

        self.log += f"status: {self._status_str(self.IDLE)}\ncabin: {cabin}\nfloor: {self.current_floor}\n\n"

        self.elevate()

    def _goto_closest(self) -> int:
        self.log += "Going to the closest passenger...\n\n"

        if self.current_floor in self.route:
            return self.current_floor

        up_probe = self.current_floor
        down_probe = self.current_floor

        for floor_number in range(self.floor_count):
            up_probe += self.UP
            down_probe += self.DOWN

            self.movement += 1

            if up_probe in self.route:
                return up_probe

            if down_probe in self.route:
                return down_probe

    def _get_status(self, destination: int) -> int:

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

    def _status_str(self, status: int):
        return {1: "UP", 0: "IDLE", -1: "DOWN"}.get(status, "UNDER MAINTENANCE!")


route = [(1, 5), (2, 4), (3, 1)]
route = dict(route)
elevator = Elevator(route)
elevator.elevate()
print(elevator.log)
