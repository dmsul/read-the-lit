import pytest

from url_dict import get_volume


def test_get_volume_normal():
    assert get_volume(2015, 'qje') == 130


def test_get_volume_normal_raise_exception_on_invalid_year():
    with pytest.raises(ValueError):
        get_volume(1800, 'ecpolicy')


def test_get_volume_multiple():
    assert get_volume(2015, 'joe', 'sep') == 188


def test_get_volume_multiple_raise_exception_on_invalid_month():
    with pytest.raises(ValueError):
        get_volume(2015, 'jue', 'oct')
