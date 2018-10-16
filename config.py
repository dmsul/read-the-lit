import pandas as pd

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
          'Nov', 'Dec']
YEAR0 = 2015


def publication_months(journal_name):
    df = publication_info()
    df = df.set_index('name')
    journal_schedule = df.loc[journal_name, months]
    journal_months = journal_schedule[journal_schedule].index.tolist()

    return journal_months


def publication_info():
    df = pd.read_csv('journal_schedule.csv')
    for month in months:
        df[month] = df[month].fillna(0).replace('X', 1).astype(bool)

    return df
