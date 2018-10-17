import pytest

from get_url import get_url


def test_get_url_1():
    test_url = "https://academic.oup.com/qje/issue/130/2"
    assert get_url('QJE', 2015, 5) == test_url


def test_get_url_2():
    with pytest.raises(ValueError):
        get_url('QJE', 1800, 5)


def test_get_url_3():
    with pytest.raises(ValueError):
        get_url('JPE', 2015, 3)


def test_get_url_4():
    test_url = ("https://www.sciencedirect.com/journal/"
                "journal-of-urban-economics/vol/88/issue/0")
    assert get_url('JUE', 2015, 7) == test_url


def test_get_url_5():
    with pytest.raises(ValueError):
        get_url('JEEM', 2015, 2)
