import pytest

journal_issue_url = {
    'qje': 'https://academic.oup.com/qje/issue/{vol}/{iss}',
    'restud': 'https://academic.oup.com/restud/issue/{vol}/{iss}',
    'restat': 'https://www.mitpressjournals.org/toc/rest/{vol}/{iss}',
    'jpe': 'https://www.journals.uchicago.edu/toc/jpe/{yr}/{vol}/{iss}',
    'jaere': 'https://www.journals.uchicago.edu/toc/jaere/{yr}/{vol}/{iss}',
    'jeem': ('https://www.sciencedirect.com/journal/journal-of-environmental-'
             'economics-and-management/vol/{vol}/issue/{iss}'),
    'jpube': ('https://www.sciencedirect.com/'
              'journal/journal-of-public-economics/vol/{vol}/issue/{iss}'),
    'jue': ('https://www.sciencedirect.com/journal/'
            'journal-of-urban-economics/vol/{vol}/issue/{iss}'),
    'ecma': 'https://onlinelibrary.wiley.com/toc/14680262/{yr}/{vol}/{iss}',
    'jole': 'https://www.journals.uchicago.edu/toc/jole/{yr}/{vol}/{iss}',
    'energy policy': ('https://www.sciencedirect.com/journal/'
                      'energy-policy/vol/{vol}/issue/{iss}'),
    'ecpolicy': 'https://academic.oup.com/economicpolicy/issue/{vol}/{iss}',
    'ecletters': ('https://www.sciencedirect.com/journal/'
                  'economics-letters/vol/{vol}/issue/{iss}'),
    'joe': ('https://www.sciencedirect.com/journal/'
            'journal-of-econometrics/vol/{vol}/issue/{iss}'),
    'jae': 'https://onlinelibrary.wiley.com/toc/10991255/{yr}/{vol}/{iss}',
    'rand': 'https://onlinelibrary.wiley.com/toc/17562171/{yr}/{vol}/{iss}',
    'jbes': 'https://amstat.tandfonline.com/toc/ubes20/{vol}/{iss}?nav=tocList'
}

journal_yr_v = {
    'qje': (2018, 133),
    'restud': (2018, 85),
    'restat': (2018, 100),
    'jpe': (2018, 126),
    'jaere': (2018, 5),
    'ecma': (2018, 86),
    'jole': (2018, 36),
    'ecpolicy': (2018, 33),
    'jae': (2018, 33),
    'rand': (2018, 49),
    'jbes': (2018, 36)
}

journal_yr_mo_v_rate = {
    'jeem': (2018, 11, 92, 6),
    'jpube': (2018, 11, 167, 12),
    'jue': (2018, 11, 108, 6),
    'energy policy': (2018, 12, 123, 12),
    'ecletters': (2018, 12, 173, 12),
    'joe': (2018, 11, 207, 6)
}

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
          'nov', 'dec']
nums = list(range(1, 13))
month_nums = dict(zip(months, nums))
inv_month_nums = {nums: months for months, nums in month_nums.items()}


def get_volume(input_y, journal_name, input_m=None):
    if journal_name in journal_yr_v:
        base_y, base_v = journal_yr_v[journal_name]
        start_y = base_y - base_v + 1
        if input_y < start_y:
            raise ValueError(f" You entered a year before {start_y}")
        offset = base_y - input_y
        vol_num = base_v - offset
        return vol_num
    else:
        base_y, base_m, base_v, ann_rate = journal_yr_mo_v_rate[journal_name]
        month_gap = 12 // ann_rate
        input_m = month_nums[input_m.lower()]
        if (base_m - input_m) % month_gap != 0:
            raise ValueError(f"Volumes only come every {month_gap} months")
        offset = (base_m - input_m) / month_gap
        offset += (base_y - input_y) * ann_rate
        vol_num = int(base_v - offset)
        return vol_num


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
