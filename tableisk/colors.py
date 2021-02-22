def _mkcolor(num):
    return "\033[" + str(num) + "m"


class TextColors:
    BLACK = _mkcolor(30)
    RED = _mkcolor(31)
    GREEN = _mkcolor(32)
    YELLOW = _mkcolor(33)
    BLUE = _mkcolor(34)
    MAGENTA = _mkcolor(35)
    CYAN = _mkcolor(36)
    WHITE = _mkcolor(37)

    BRIGHT_BLACK = _mkcolor(90)
    BRIGHT_RED = _mkcolor(91)
    BRIGHT_GREEN = _mkcolor(92)
    BRIGHT_YELLOW = _mkcolor(93)
    BRIGHT_BLUE = _mkcolor(94)
    BRIGHT_MAGENTA = _mkcolor(95)
    BRIGHT_CYAN = _mkcolor(96)
    BRIGHT_WHITE = _mkcolor(97)

    RESET = _mkcolor(0)

    NONE = ""
