import typing

from .colors import TextColors


def display(data):
    table = Table(data)
    text = table.formatted_text()
    print(text)


class Cell:
    def __init__(self, data: typing.Any):
        """
        Args:
            data: data to store display in this cell. Data item is immediately converted to string.
        """
        # TODO: Should we do deferred string conversion?
        self.text = str(data)

    def cell_width(self) -> int:
        return len(self.text)

    def formatted_text(self, width=None):
        width = len(self.text) if not width else width
        return f"{TextColors.RED}{self.text:<{width}}{TextColors.RESET}"

    def __eq__(self, other):
        if isinstance(other, Cell):
            return self == other.text
        else:
            return self.text == str(other)

    def __repr__(self) -> str:
        return self.text


class _RowView:
    def __init__(self, table_data):
        self.data = table_data

    def __getitem__(self, index) -> typing.List[Cell]:
        return self.data[index]

    def __len__(self) -> int:
        return len(self.data)


class _ColView:
    def __init__(self, table_data, headers):
        self.data = table_data
        self._header_map = {name: i for i, name in enumerate(headers)}

    def __getitem__(self, name_or_index) -> typing.List[Cell]:
        index = self._header_map[name_or_index] if isinstance(name_or_index, str) else name_or_index
        return _Col([row[index] for row in self.data])


class _Col:
    def __init__(self, col_cells: typing.List[Cell]):
        self._cells = col_cells

    def cell_widths(self) -> typing.List[int]:
        return [cell.cell_width() for cell in self._cells]

    def __eq__(self, other):
        if isinstance(other, list):
            return other == self._cells
        elif isinstance(other, _Col):
            return other._cells == self._cells
        else:
            raise TypeError(f"Cannot equality compare types {other.__class__} and {self.__class__}")


class Table:
    def __init__(self, data: typing.List[typing.List[typing.Any]], headers=None):
        if headers is None:
            self._raw_data = data[1:]
            self._headers = data[0]
        else:
            self._raw_data = data
            self._headers = headers

        # self.data = [Row(row) for row in self._raw_data]
        self.data = []
        for row in self._raw_data:
            new_row = []
            for item in row:
                new_row.append(Cell(item))
            self.data.append(new_row)

    @property
    def rows(self) -> _RowView:
        return _RowView(self.data)

    @property
    def cols(self) -> _ColView:
        return _ColView(self.data, self._headers)

    def formatted_text(self):
        # Collect widths for each row, and set final widths to max of each
        default_widths = [row.cell_widths() for row in self.rows]

        transposed_widths = list(zip(*default_widths))
        max_widths = [max(col) for col in transposed_widths]

        text = "\n".join([row.formatted_text(max_widths) for row in self.rows])
        return text


# class Row:
#     def __init__(self, data_elems: typing.List[typing.Any]):
#         self.cells = [Cell(elem) for elem in data_elems]

#     def cell_widths(self) -> typing.List[int]:
#         return [cell.cell_width() for cell in self.cells]

#     def formatted_text(self, widths: typing.List[int] = None):

#         if widths is None:
#             widths = [None] * len(self.cells)

#         text = " | ".join([cell.formatted_text(width) for cell, width in zip(self.cells, widths)])

# return text
