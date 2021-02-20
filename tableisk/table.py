import typing


def display(data):
    table = Table(data)
    print(table.formatted_text())


class Table:
    def __init__(self, data: typing.List[typing.List[typing.Any]]):
        self.rows = [Row(row) for row in data]

    def formatted_text(self):
        # Collect widths for each row, and set final widths to max of each
        default_widths = [row.cell_widths() for row in self.rows]

        transposed_widths = list(zip(*default_widths))
        max_widths = [max(col) for col in transposed_widths]

        text = "\n".join([row.formatted_text(max_widths) for row in self.rows])
        return text


class Row:
    def __init__(self, data_elems: typing.List[typing.Any]):
        self.cells = [Cell(elem) for elem in data_elems]

    def cell_widths(self) -> typing.List[int]:
        return [cell.cell_width() for cell in self.cells]

    def formatted_text(self, widths: typing.List[int] = None):

        if widths is None:
            widths = [None] * len(self.cells)

        text = " | ".join([cell.formatted_text(width) for cell, width in zip(self.cells, widths)])

        return text


class Cell:
    def __init__(self, text: typing.Any):
        self.text = text

    def cell_width(self) -> int:
        return len(self.text)

    def formatted_text(self, width=None):
        width = len(self.text) if not width else width
        return f"{self.text:<{width}}"
