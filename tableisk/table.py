import shutil
import typing
import textwrap
from .colors import TextColors


def _get_terminal_width(fallback=120):
    return shutil.get_terminal_size(fallback=(fallback, 40)).columns


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
        self.width = None

    def cell_width(self) -> int:
        return max(map(len, self._text_lines()))

    def desired_width(self):
        """A Cell's desired with is how long it's full input text is with no wrapping"""
        return len(self.text)

    def min_width(self):
        """A Cell's min with is the smallest a cell can be without breaking words in work wrapping.
        i.e. it is the length of the longest single token"""
        return max(map(len, self.text.split()))

    def _text_lines(self, width=None) -> typing.List[str]:
        width = self.desired_width() if not width else width
        split_lines = textwrap.wrap(self.text, width=width)
        return split_lines

    def formatted_text(self, width=None):
        width = self.desired_width() if not width else width
        lines = self._text_lines(width)
        lines = [f"{txt:<{width}}" for txt in lines]
        return lines
        # return f"{TextColors.RED}{self.text:<{width}}{TextColors.RESET}"

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

    def __iter__(self):
        for row in self.data:
            yield _RowView(row)


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

        self.rows = _RowView(self.data)
        self.cols = _ColView(self.data, self._headers)

    def formatted_text(self):
        # Collect widths for each row, and set final widths to max of each
        max_widths = [max(col.cell_widths()) for col in self.cols]

        text = []
        for row in self.rows:
            # Get each cell's text, but if it's wraps, we'll need to pad everything to same size for easy printing

            cell_texts = [cell.formatted_text(width) for cell, width in zip(row.data, max_widths)]

            wrapped_rows = max(map(len, cell_texts))

            padded_texts = []
            for texts, width in zip(cell_texts, max_widths):
                rows_to_add = wrapped_rows - len(texts)
                padded_texts.append(texts + [f"{'':<{width}}"] * rows_to_add)

            for line_of_text in zip(*padded_texts):
                row_text = " | ".join(line_of_text)
                text.append(row_text)

        text = "\n".join(text)
        return text
