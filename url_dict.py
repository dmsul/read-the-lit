from config import months, publication_months

journal_url = {
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

journal_yr_vol = {
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

journal_yr_mo_vol = {
    'jeem': (2018, 'Nov', 92),
    'jpube': (2018, 'Nov', 167),
    'jue': (2018, 'Nov', 108),
    'energy policy': (2018, 'Dec', 123),
    'ecletters': (2018, 'Dec', 173),
    'joe': (2018, 'Nov', 207)
}


def get_url(journal_name, input_y, input_m):
    pub_months = publication_months(journal_name)
    journal_name = journal_name.lower()

    if journal_name in journal_yr_vol:
        base_y, base_v = journal_yr_vol[journal_name]
        start_y = base_y - base_v + 1
        if input_y < start_y:
            raise ValueError(f"You entered a year before {start_y}")

        offset = base_y - input_y
        vol_num = base_v - offset
        if input_m not in pub_months:
            raise ValueError(f"Publishing months are: {pub_months}.")

        issue_num = pub_months.index(input_m) + 1
        url = journal_url[journal_name]
        return url.format(vol=vol_num, iss=issue_num, yr=input_y)

    else:
        base_y, base_m, base_v = journal_yr_mo_vol[journal_name]

        month_gap = 12 // len(pub_months)
        if input_m not in pub_months:
            raise ValueError(f"Publishing months are: {pub_months}")
        input_m = months.index(input_m) + 1
        base_m = months.index(base_m) + 1

        offset = (base_m - input_m) / month_gap
        offset += (base_y - input_y) * len(pub_months)
        vol_num = int(base_v - offset)
        url = journal_url[journal_name]

        return url.format(vol=vol_num, iss=0)
