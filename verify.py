from typing import Text
import tableisk
from tableisk import table as tb
from tableisk.colors import BackgroundColors, TextColors


def red(cell, col, row):
    # return tableisk.CellColor(TextColors.RED, BackgroundColors.BLUE)
    if "row" in cell.text:
        return tableisk.CellColor(TextColors.RED, BackgroundColors.BLUE)
    else:
        return tableisk.CellColor(None, None)


def simple_table():
    data = [
        ["Num", "Letters", "Description"],
        ["1", "aaa", "first row"],
        ["20", "bb", "second row"],
        ["300", "c", "third row"],
    ]

    table = tableisk.Table(data)
    table.cols["Description"].formatter = red

    as_string = tb._output_table_bash(table)
    print(as_string)
    # tableisk.display(data)


if __name__ == "__main__":
    simple_table()
