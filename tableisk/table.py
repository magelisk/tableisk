import shutil
import typing
import textwrap
from collections import namedtuple

from .colors import TextColors, BackgroundColors


def _get_terminal_width(fallback=120):
    return shutil.get_terminal_size(fallback=(fallback, 40)).columns


def display(data):
    table = Table(data)
    text = _output_table_bash_console(table)
    # text = table.formatted_text()
    print(text)


# CellColor = namedtuple("CellColor", ["text_color", "background_color"])
class CellColor(typing.NamedTuple):
    text: TextColors
    background: BackgroundColors


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

    def color_formatter(self, formatter: typing.Callable):
        """Takes a callable function with the signature:

        ::
          def formatter(cell: Cell, column: List[Cell], row: List[Cell], current_format: CellColor) -> CellColor

        The content of CellColor defines the text color and background color to use for this cell.
        Because multiple formatters can apply to the same cell, they will be evaluated in the order of
        Row --> Col --> Cell with later ones overriding earlier ones. Therefore:
        * If you wish to return no change/take no action in a formatter, set the field in CellColor to None
        * If you wish to explicitly remove any other formatting, set the field in CellColor to
          the appropriate RESET value
        """
        self._formatter = formatter

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
        self._headers = headers
        self._header_map = {header.text: i for i, header in enumerate(headers)}
        # TODO: Premake _Col entries so we can preserve formatter functions

    def __getitem__(self, name_or_index) -> typing.List[Cell]:
        index = self._header_map[name_or_index] if isinstance(name_or_index, str) else name_or_index
        header_cell = self._headers[index]
        return _Col([row[index] for row in self.data], header_cell)


class _Col:
    def __init__(self, col_cells: typing.List[Cell], header_cell: Cell):
        self._cells = col_cells
        self._header_cell = header_cell

    def cell_widths(self) -> typing.List[int]:
        return [self._header_cell.cell_width()] + [cell.cell_width() for cell in self._cells]

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
            self._raw_headers = data[0]
        else:
            self._raw_data = data
            self._raw_headers = headers

        self._headers = [Cell(cell) for cell in self._raw_headers]

        self.data = []
        for row in self._raw_data:
            new_row = []
            for item in row:
                new_row.append(Cell(item))
            self.data.append(new_row)

        self.rows = _RowView(self.data)
        self.cols = _ColView(self.data, self._headers)

    # def formatted_text(self):
    #     # Collect widths for each row, and set final widths to max of each
    #     max_widths = [max(col.cell_widths()) for col in self.cols]

    #     text = []

    #     # Render header
    #     # TODO: Pull this render logic into separate function so it's not so copy/paste
    #     cell_texts = [cell.formatted_text(width) for cell, width in zip(self._headers, max_widths)]
    #     num_wrapped_rows = max(map(len, cell_texts))
    #     padded_texts = [_pad_text_list(texts, num_wrapped_rows, width) for texts, width in zip(cell_texts, max_widths)]
    #     text += _join_table_row(padded_texts)

    #     for row in self.rows:
    #         # Get each cell's text, but if it's wraps, we'll need to pad everything to same size for easy printing
    #         cell_texts = [cell.formatted_text(width) for cell, width in zip(row.data, max_widths)]

    #         num_wrapped_rows = max(map(len, cell_texts))

    #         padded_texts = [
    #             _pad_text_list(texts, num_wrapped_rows, width) for texts, width in zip(cell_texts, max_widths)
    #         ]

    #         text += _join_table_row(padded_texts)

    #     text = "\n".join(text)
    #     return text


def _pad_text_list(original_text_list, desired_size, padding_width, padding_char="") -> typing.List[str]:
    rows_to_add = desired_size - len(original_text_list)
    return original_text_list + [f"{padding_char*padding_width}"] * rows_to_add


def _join_table_row(cell_texts: typing.List[typing.List[str]]) -> typing.List[str]:
    """Takes the wrapped text lists for each cell, and joins them together aligning rows
    and putting appropriate separators between each cell's entry

    Example:

    ::
      [
          ["Cell", "One ", "text"],
          ["Second", "Text  ", "     "]
      ]

    Becomes:

    ::
      Cell | Second
      One  | Text
      Test |
    """

    row_counts = list(map(len, cell_texts))
    if not all([count == row_counts[0] for count in row_counts]):
        raise ValueError(f"Each entry of cell_text must be the same size. Got cell_texts with sizes {row_counts}")

    lines = []
    for line_of_text in zip(*cell_texts):
        row_text = " | ".join(line_of_text)
        lines.append(row_text)
    return lines


def _generate_row_text_lines(row, widths):
    cell_texts = [cell.formatted_text(width) for cell, width in zip(row, widths)]
    num_wrapped_rows = max(map(len, cell_texts))
    padded_texts = [_pad_text_list(texts, num_wrapped_rows, width) for texts, width in zip(cell_texts, widths)]
    return _join_table_row(padded_texts)


def _output_table_bash_console(table: Table):
    # Collect widths for each row, and set final widths to max of each
    max_widths = [max(col.cell_widths()) for col in table.cols]

    text = []

    text = _generate_row_text_lines(table._headers, max_widths)

    for row in table.rows:
        text += _generate_row_text_lines(row.data, max_widths)

    text = "\n".join(text)
    return text
