import tableisk


def simple_table():
    data = [
        ["Num", "Letters", "Description"],
        ["1", "aaa", "first row"],
        ["20", "bb", "second row"],
        ["300", "c", "third row"],
    ]
    tableisk.display(data)


if __name__ == "__main__":
    simple_table()
