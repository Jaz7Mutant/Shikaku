"""
Colors for blocks and text, methods for colorizing
"""
from colorama import Back, Fore

BACK_COLORS = {
    -1: Back.RESET,
    0: Back.RED,
    1: Back.BLUE,
    2: Back.GREEN,
    3: Back.YELLOW,
    4: Back.WHITE,
    5: Back.MAGENTA,
    6: Back.CYAN,
    7: Back.LIGHTWHITE_EX,
    8: Back.LIGHTBLACK_EX,
    9: Back.LIGHTYELLOW_EX,
    10: Back.LIGHTRED_EX,
    11: Back.LIGHTGREEN_EX,
    12: Back.LIGHTCYAN_EX,
    13: Back.LIGHTBLUE_EX,
    14: Back.LIGHTMAGENTA_EX,
}

FORE_COLORS = {
    -1: Fore.RESET,
    0: Fore.BLACK,
    1: Fore.WHITE,
    2: Fore.RED
}


def colorize_back(line: str, color: Back) -> str:
    """ returns string with colorized background"""
    return color + line + BACK_COLORS[-1]


def colorize_front(line: str, color: Fore) -> str:
    """ returns string with colorized foreground"""
    return color + line + FORE_COLORS[-1]
