from src.teams import create


def test_create_teams_2_even():
    names = ["test1", "test2", "test3", "test4", "test5", "test6"]
    assert create(names, 2, _dummy_shuffle) == [
        ["test6", "test4", "test2"],
        ["test5", "test3", "test1"],
    ]


def test_create_teams_2_without_shuffle_function():
    names = ["test1", "test2", "test3", "test4", "test5", "test6"]
    assert create(names, 2) == [
        ["test1", "test3", "test5"],
        ["test2", "test4", "test6"],
    ]


def test_create_teams_3_even():
    names = ["test1", "test2", "test3", "test4", "test5", "test6"]
    assert create(names, 3, _dummy_shuffle) == [
        ["test6", "test3"],
        ["test5", "test2"],
        ["test4", "test1"],
    ]


def test_create_teams_3_uneven():
    names = ["test1", "test2", "test3", "test4", "test5"]
    assert create(names, 3, _dummy_shuffle) == [
        ["test5", "test2"],
        ["test4", "test1"],
        ["test3"],
    ]


def test_create_teams_4_uneven():
    names = ["test1", "test2", "test3", "test4", "test5", "test6"]
    assert create(names, 4, _dummy_shuffle) == [
        ["test6", "test2"],
        ["test5", "test1"],
        ["test4"],
        ["test3"],
    ]


def test_create_teams_empty_input():
    names = []
    assert create(names, 2, _dummy_shuffle) == []


def test_create_teams_less_names_than_teams():
    names = ["test6", "test5", "test4", "test3", "test2", "test1"]
    assert create(names, len(names) + 1, _dummy_shuffle) == names


def _dummy_shuffle(l):
    l.reverse()
