
passengers = [(1, 5), (2, 4), (3, 1)]


class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, start_floor: int = 1) -> None:
        self.current_floor = start_floor
        self.status = self.IDLE

    def elevate(self, passengers: list) -> None:
        passengers = dict(passengers)
        cabin = []

        self.current_floor = self.goto_closest(passengers)

        cabin.append(self.current_floor)

        destination = passengers[self.current_floor]

        self.status = self.get_status(destination)

        while len(cabin) != 0:
            self.current_floor += self.status

            if self.current_floor in passengers \
                    and self.get_status(passengers[self.current_floor]) == self.status:

                cabin.append(self.current_floor)

            for passenger in cabin:
                destination = passengers[passenger]

                if self.current_floor == destination:
                    cabin.remove(passenger)

    def goto_closest(self, passengers: dict) -> int:

        if self.current_floor in passengers:
            return self.current_floor

        up_probe = self.current_floor
        down_probe = self.current_floor

        for passenger in passengers.keys():
            up_probe += self.UP
            down_probe += self.DOWN

            if up_probe in passengers:
                return up_probe

            if down_probe in passengers:
                return down_probe

    def get_status(self, destination):
        if self.current_floor == destination:
            return self.IDLE

        if self.current_floor > destination:
            return self.DOWN

        if self.current_floor < destination:
            return self.UP


e = Elevator()
e.elevate(passengers)
