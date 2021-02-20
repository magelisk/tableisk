import typing


def display(data):
    table = Table(data)
    print(table.formatted_text())


class Table:
    def __init__(self, data: typing.List[typing.List[typing.Any]]):
        self.rows = [Row(row) for row in data]

    def formatted_text(self):
        text = " | ".join([cell.formatted_text() for cell in self.cells])
        return text


class Row:
    def __init__(self, data_elems: typing.List[typing.Any]):
        self.cells = [Cell(elem) for elem in data_elems]

    def formatted_text(self):
        text = " | ".join([cell.formatted_text() for cell in self.cells])
        return text


class Cell:
    def __init__(self, text: typing.Any):
        self.text = text

    def formatted_text(self):
        return self.text
