from cli.helpers.utils import filter_dict


def test_filter_dict():
    d = {"a": 1, "b": 2}

    filtered_d = filter_dict(d, lambda v: v > 1)
    assert filtered_d == {"b": 2}
