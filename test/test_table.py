import pytest

from tableisk import Table, Cell, Row
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


def test_table_init_rows_and_cols(sample_data_no_wrap):
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
    ce = Cell("my content")
    assert ce != "my content2"

    ce2 = Cell("my content2")
    assert ce != ce2
    assert ce2 != ce
