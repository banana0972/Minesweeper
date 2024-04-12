import random
from typing import TypeVar

# T = TypeVar("T")

Point = (int, int)
Board = list[list[int]]
Field = list[list[bool]]
width: int
height: int

# TESTING ONLY REMOVEME
# random.seed(0)


def generate[T](w: int, h: int, default: T) -> list[list[T]]:
    board = []
    for i in range(h):
        board.append([default] * w)
    return board


def populate_field(field: Field, mines: int):
    placed = 0
    while placed < mines:
        # Pick a random coord
        x, y = random.randint(0, width - 1), random.randint(0, height - 1)
        # Ensure there is no mine already
        if not field[y][x]:
            if population_check(field, x, y):
                continue
            placed += 1
            field[y][x] = True


def repopulate(field: Field, x: int, y: int):
    attempt = 0
    count = count_mines(field, x, y, True)
    while count != 0:
        set_index(field, x-1, y+1, False)
        set_index(field, x, y+1, False)
        set_index(field, x+1, y+1, False)
        set_index(field, x-1, y, False)
        set_index(field, x, y, False)
        set_index(field, x+1, y-1, False)
        set_index(field, x, y-1, False)
        set_index(field, x-1, y-1, False)
        populate_field(field, count)
        count = count_mines(field, x, y, True)
        attempt += 1
        print(f"Repopulation attempt {attempt}, there were {count} mines")

def population_check(field: Field, x: int, y: int) -> bool:
    """
    :return: True if the mine is in a horrible place
    """
    # Check for surrounding mines
    # A setup like
    # XXX
    # XXX
    # XXX
    # would be horrible
    return (get_index(field, x - 1, y + 1, True) and get_index(field, x, y + 1, True) and get_index(field, x + 1, y + 1, True) and
            get_index(field, x - 1, y, True) and get_index(field, x + 1, y, True) and
            get_index(field, x - 1, y - 1, True) and get_index(field, x, y - 1, True) and get_index(field, x + 1, y - 1, True))


def set_index[T](board: list[list[T]], x: int, y: int, item: T):
    if (x < 0 or x >= width) or (y < 0 or y >= width):
        return
    board[y][x] = item


def get_index[T](board: list[list[T]], x: int, y: int, default: T = None) -> T:
    if (x < 0 or x >= width) or (y < 0 or y >= width):
        return default
    return board[y][x]


def print_field(field: Field):
    for row in reversed(field):
        print("".join("X" if mine else "-" for mine in row))


def print_board(board: Board):
    for row in reversed(board):
        print("".join(str(count) if count != -1 else " " for count in row))


def count_mines(field: Field, x: int, y: int, center: bool = False) -> int:
    surrounding = 0
    surrounding += get_index(field, x - 1, y + 1, False) + get_index(field, x, y + 1, False) + get_index(field, x + 1,
                                                                                                         y + 1, False)
    surrounding += get_index(field, x - 1, y, False) + get_index(field, x + 1, y, False)
    if center and get_index(field, x, y):
        surrounding += 1
    surrounding += get_index(field, x - 1, y - 1, False) + get_index(field, x, y - 1, False) + get_index(field, x + 1,
                                                                                                         y - 1, False)
    return surrounding


def interact(board: Board, field: Field, flags: Field, x: int, y: int, checked: list[Point]) -> bool:
    # Skip interaction if already checked or if tile is flagged
    if (x, y) in checked or get_index(flags, x, y):
        return False
    # print(f"Checking {x, y}")
    checked.append((x, y))
    # Anything out of bounds does nothing
    if (x < 0 or x >= width) or (y < 0 or y >= width):
        return False
    # Kaboom
    if get_index(field, x, y):
        return True
    surrounding = count_mines(field, x, y)
    set_index(board, x, y, surrounding)
    # Exposed tiles can be interacted with if there are the correct number of flags
    if get_index(board, x, y, -1) != -1:
        # Flags are treated as discovered mines
        surrounding -= count_mines(flags, x, y)
    explode = False
    # If a tile was misflagged, there is a chance of kaboom
    if surrounding == 0:
        # Recursively reveal tiles
        # Top
        explode |= interact(board, field, flags, x - 1, y + 1, checked)
        explode |= interact(board, field, flags, x, y + 1, checked)
        explode |= interact(board, field, flags, x + 1, y + 1, checked)
        # Mid
        explode |= interact(board, field, flags, x - 1, y, checked)
        explode |= interact(board, field, flags, x + 1, y, checked)
        # Bottom
        explode |= interact(board, field, flags, x - 1, y - 1, checked)
        explode |= interact(board, field, flags, x, y - 1, checked)
        explode |= interact(board, field, flags, x + 1, y - 1, checked)
    return explode


if __name__ == '__main__':
    width = 16
    height = 16
    game_board = generate(width, height, -1)
    mines = generate(width, height, False)
    flags = generate(width, height, False)
    populate_field(mines, 40)
    print_field(mines)
    print("---")
    print_board(game_board)
    print("---")
    # 0 mine
    interact(game_board, flags, mines, 1, 0, [])
    # 1 mine
    # print(interact(game_board, mines, 6, 0, []))
    print("BOARD")
    print_board(game_board)
    # print(interact(game_board, mines, 7, 0, []))
