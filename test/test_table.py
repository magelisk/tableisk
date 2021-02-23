import pytest

from tableisk import Table, Cell
from tableisk.table import _RowView, _ColView


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
    col = _ColView(sample_data, ["first", "second"])
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

    assert presized_colview["first"].cell_widths() == [5, 10]
    assert presized_colview["second"].cell_widths() == [3, 1]
