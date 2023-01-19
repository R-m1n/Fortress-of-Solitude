

class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, passengers: dict, start_floor: int = 1) -> None:
        self.passengers = passengers
        self.passenger_count = len(passengers)
        self.current_floor = start_floor
        self.status = self.IDLE

    def elevate(self) -> None:

        if len(self.passengers) == 0:
            return

        cabin = []

        self.current_floor = self.goto_closest()

        cabin.append(self.current_floor)

        destination = self.passengers[self.current_floor]

        self.status = self.get_status(destination)

        print(f"cabin: {cabin} -> floor: {self.current_floor}")

        while len(cabin) != 0:
            self.current_floor += self.status

            if self.current_floor in self.passengers \
                    and (self.get_status(self.passengers[self.current_floor]) == self.status
                         or self.get_status(self.passengers[self.current_floor]) == self.IDLE):

                cabin.append(self.current_floor)

            print(f"cabin: {cabin} -> floor: {self.current_floor}")

            for passenger in cabin:
                destination = self.passengers[passenger]

                if self.current_floor == destination or destination == 0:
                    cabin.remove(passenger)
                    self.passengers.pop(passenger)

        print(f"cabin: {cabin} -> floor: {self.current_floor}")

        self.elevate()

    def goto_closest(self) -> int:

        if self.current_floor in self.passengers:
            return self.current_floor

        up_probe = self.current_floor
        down_probe = self.current_floor

        for i in range(self.passenger_count):
            up_probe += self.UP
            down_probe += self.DOWN

            if up_probe in self.passengers:
                return up_probe

            if down_probe in self.passengers:
                return down_probe

    def get_status(self, destination):

        if self.current_floor == destination or destination == 0:
            return self.IDLE

        if self.current_floor > destination:
            return self.DOWN

        if self.current_floor < destination:
            return self.UP


passengers = [(1, 5), (2, 0), (3, 1)]
passengers = dict(passengers)
e = Elevator(passengers)
e.elevate()
