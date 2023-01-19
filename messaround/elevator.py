

class Elevator():
    UP = 1
    IDLE = 0
    DOWN = -1

    def __init__(self, route: dict, start_floor: int = 1) -> None:
        self.route = route
        self.floor_count = max(route.values())
        self.current_floor = start_floor
        self.status = self.IDLE
        self.log = f"\nPassengers waiting on floors: {list(route.keys())}\n\nCurrent floor: {self.current_floor}\n"
        self.movement = 0

    def elevate(self) -> None:

        if len(self.route) == 0:
            return

        cabin = []

        self.current_floor = self.goto_closest()

        cabin.append(self.current_floor)

        destination = self.route[self.current_floor]

        self.status = self.get_status(destination)

        self.log += f"cabin: {cabin}\t\t\t\tfloor: {self.current_floor}\n"

        while len(cabin) != 0:
            self.current_floor += self.status

            self.movement += 1

            if self.current_floor in self.route \
                    and (self.get_status(self.route[self.current_floor]) == self.status
                         or self.get_status(self.route[self.current_floor]) == self.IDLE):

                cabin.append(self.current_floor)

            self.log += f"cabin: {cabin}\t\t\t\tfloor: {self.current_floor}\n"

            for passenger in cabin:
                destination = self.route[passenger]

                if self.current_floor == destination or destination == self.IDLE:
                    cabin.remove(passenger)
                    self.route.pop(passenger)

        self.log += f"cabin: {cabin}\t\t\t\tfloor: {self.current_floor}\n"

        self.elevate()

    def goto_closest(self) -> int:
        self.log += "\nFinding closest passenger...\n\n"

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

    def get_status(self, destination):

        if self.current_floor == destination or destination == self.IDLE:
            return self.IDLE

        if self.current_floor > destination:
            return self.DOWN

        if self.current_floor < destination:
            return self.UP


route = [(1, 5), (2, 0), (3, 1)]
route = dict(route)
elevator = Elevator(route)
elevator.elevate()
print(elevator.log)
print(f"Total movements: {elevator.movement}")
