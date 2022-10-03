
class Disk():
    position = 0

    def __init__(self, digits: list):
        self.disk = digits

    def __repr__(self) -> str:
        return " ".join(list(map(lambda digit: str(digit), self.disk)))

    def rotate(self) -> None:
        rotated_disk = [self.disk[-1]]
        for i in self.disk[:len(self.disk)-1]:
            rotated_disk.append(i)
        self.disk = rotated_disk
        self.reset_position()

    def get_disk(self) -> list:
        return self.disk

    def get_scope(self) -> list:
        return self.disk[1:-1]

    def get_position(self) -> int:
        return self.position

    def isfull(self) -> bool:
        if self.position == len(self.disk) - 1:
            return True
        else:
            return False

    def reset_position(self) -> None:
        if self.isfull():
            self.position = 0
        else:
            self.position += 1


def unlock(top_disk: Disk, bot_disk: Disk):
    while not (top_disk.isfull() and bot_disk.isfull()):
        top_scope = top_disk.get_scope()
        bot_scope = bot_disk.get_scope()
        combination = ""

        if bot_disk.isfull():
            top_disk.rotate()

        for i in range(len(top_scope)):
            combination += str((top_scope[i] + bot_scope[i]) % 10)

        if int(combination) % 6 == 0:
            result = f"\nUnlocked :) \
                       \n\nRotate Top Disk {top_disk.get_position()} time(s).\
                       \nRotate Bot Disk {bot_disk.get_position()} time(s).\
                       \n\nTop Disk: {top_disk} \
                       \nBot Disk: {bot_disk}"
            print(result)
            break

        else:
            bot_disk.rotate()

    else:
        print("\nThe Lock is Rigged :(")


if __name__ == "__main__":
    td = Disk(list(map(lambda digit: int(digit),
                   input("Top Disk Digits: ").strip().split(" "))))
    bd = Disk(list(map(lambda digit: int(digit),
                   input("Bot Disk Digits: ").strip().split(" "))))

    unlock(td, bd)
