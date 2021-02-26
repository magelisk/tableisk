import pytest

from tableisk import Table, Cell
from tableisk import table


def _transpose(data):
    return list(map(list, zip(*data)))


@pytest.fixture
def sample_data_no_wrap():
    data = [
        ["Id", "Name", "Location", "Still Around?"],
        ["1", "Library Of Alexandria", "Egypt", "No"],
        ["33", "Eifle Tower", "Paris", "Yes"],
        ["66", "Big Ben", "London", "Yes"],
    ]
    return data


@pytest.fixture
def presized_colview():
    # Sample data of varying sizes to easily compare
    sample_data = [
        [Cell("12345"), Cell("123")],
        [Cell("1234567890"), Cell("1")],
    ]

    col = table._ColView(sample_data, [Cell("first"), Cell("second")])
    return col


def test_table_init_rows_and_cols(sample_data_no_wrap):
    """General Table initialization test to show that rows and columns are populated and accessible as expected"""
    table = Table(sample_data_no_wrap)

    # Auto grabs headers
    assert table._headers == sample_data_no_wrap[0]

    assert len(table.rows) == 3
    assert table.rows[0] == sample_data_no_wrap[1]
    assert table.rows[1] == sample_data_no_wrap[2]
    assert table.rows[2] == sample_data_no_wrap[3]

    expected_cols = _transpose(sample_data_no_wrap[1:])

    assert table.cols[0] == expected_cols[0]
    assert table.cols[1] == expected_cols[1]
    assert table.cols[2] == expected_cols[2]


def test_cell_equality_against_raw_data_ie_equal():
    """Show Cell equality works for strings and other Cell types"""
    ce = Cell("my content")
    assert ce == "my content"

    ce2 = Cell("my content")
    assert ce == ce2
    assert ce2 == ce

    class _QuirkDemo:
        def __str__(self):
            return "my content"

    assert ce == _QuirkDemo()


def test_cell_equality_against_raw_data_not_equal():
    """Show Cell equality does not match with unequal strings and other Cell types"""
    ce = Cell("my content")
    assert ce != "my content2"

    ce2 = Cell("my content2")
    assert ce != ce2
    assert ce2 != ce


def test_cell_width_no_formatting():
    """Verify cell width returns length of """
    assert Cell("1").cell_width() == 1
    assert Cell("12").cell_width() == 2
    assert Cell("1" * 100).cell_width() == 100


def test_colview_get_column_by_name(presized_colview):
    assert presized_colview[0] == presized_colview["first"]
    assert presized_colview[1] == presized_colview["second"]


def test_colview_cell_widths(presized_colview):
    """Show that _ColView 'cell_widths' returns appropriate list"""
    # duplicate assertions with both index and title lookup

    # NOTE: First element is header length!
    assert presized_colview["first"].cell_widths() == [5, 5, 10]
    assert presized_colview["second"].cell_widths() == [6, 3, 1]


def test_cell_desired_width():
    cell = Cell("12345")
    assert cell.desired_width() == 5

    cell = Cell("12345 123 12 1234567890")
    assert cell.desired_width() == 23


def test_cell_min_width():
    cell = Cell("12345")
    assert cell.min_width() == 5

    cell = Cell("12345 123 12 1234567890")
    assert cell.min_width() == 10


def test_cell_text_no_wrapping():
    """Default text output"""
    cell = Cell("This line is 15")

    text = cell.formatted_text()
    assert len(text) == 1
    assert len(text[0]) == 15


def test_cell_text_with_wrapping():
    """Test getting text for a line that does word wrapping"""
    # Default
    cell = Cell("This line is 15")

    # Split halfway
    text = cell.formatted_text(width=10)
    assert len(text) == 2

    assert len(text[0]) == 10
    assert "This line " in text[0]

    assert len(text[1]) == 10
    assert "is 15     " in text[1]

    # Split on each word
    text = cell.formatted_text(width=4)
    assert len(text) == 4
    assert "This" == text[0]
    assert "line" == text[1]
    assert "is  " == text[2]
    assert "15  " == text[3]


def test_pad_text_list_nothing_needed():
    starting = ["12345", "67890"]
    result = table._pad_text_list(starting, 2, 5)
    assert result == starting

    result = table._pad_text_list(starting, 1, 5)
    assert result == starting


@pytest.mark.parametrize("padding_char", [" ", "-", "="])
def test_pad_text_list_add_rows(padding_char):
    starting = ["12345", "67890"]
    expected_padding = padding_char * 5
    result = table._pad_text_list(starting, 4, 5, padding_char=padding_char)
    assert result[0] == starting[0]
    assert result[1] == starting[1]
    assert result[2] == expected_padding
    assert result[3] == expected_padding


def test_join_table_row():
    inputs = [["Cell", "One ", "Text"], ["Second", "Text  ", "      "]]
    result = table._join_table_row(inputs)

    expected = [
        "Cell | Second",
        "One  | Text  ",
        "Text |       ",
    ]

    assert result == expected


def test_generate_table_row_mismatched_sizes():
    assert False
