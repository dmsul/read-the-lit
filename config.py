import pandas as pd

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
          'Nov', 'Dec']
YEAR0 = 2015


class PublicationInfo(object):

    def __init__(self):
        self.pub_info = publication_info()

    def pub_months(self, journal_name: str) -> list:
        df = self.pub_info.set_index('name')
        journal_schedule = df.loc[journal_name, months]
        journal_months = journal_schedule[journal_schedule].index.tolist()

        return journal_months


def publication_info():
    df = pd.read_csv('journal_schedule.csv')
    for month in months:
        df[month] = df[month].fillna(0).replace('X', 1).astype(bool)

    return df


pub_info = PublicationInfo()


def publication_months(journal_name: str) -> list:
    return pub_info.pub_months(journal_name)
