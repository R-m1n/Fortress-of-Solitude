import sys


def diamond(length: int = 37, twin: bool = False) -> None:
    if length % 2 == 0 or length < 0:
        raise ValueError(
            "Inappropriate argument value, only positive odd integers are allowed.")

    right = left = length // 2
    increment = 2 if twin else 1

    for i in range(length):
        if right == length - 1 and left == 0:
            right, left = left, right

        base = [' '] * length
        base[right % length] = '*'
        base[left % length] = '*'
        print(''.join(base))

        right += increment
        left -= increment


if __name__ == "__main__":
    length = int(sys.argv[1])
    twin = True if sys.argv[2].lower() in ['true', 'twin'] else False

    diamond(length, twin)
