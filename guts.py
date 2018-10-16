from typing import Union
from datetime import date as make_date, datetime
from itertools import chain

import pandas as pd

from config import YEAR0, months, publication_info
from url_dict import get_url


def extrap_issues(name: str, months: list, weight: int, website: str) -> list:
    wt = -1 * weight
    mo_idx = tuple([i + 1 for i, x in enumerate(months) if x])
    issues = [
        Issue(name, make_date(y, m, 1), wt, website)
        for y in range(YEAR0, 2018 + 1)
        for m in mo_idx
    ]

    # Drop future issues
    TODAY = datetime.today()
    issues = [x for x in issues if diff_in_months(TODAY, x.date) >= 0]

    return issues


class Issue(object):

    def __init__(self, name: str, date: make_date, weight: int,
                 website: str) -> None:
        self.name = name
        self.date = date
        self.weight = weight
        self.journal_website = website
        self._website = ''

    def __repr__(self) -> str:
        return '{} {}'.format(self.name, self.date.strftime('%Y %b'))

    def __sub__(self, other):
        return (.4 * (self.weight - other.weight) +    # noqa
                .6 * (diff_in_months(self.date, other.date)))

    def __eq__(self, other):
        return self.date == other.date and self.weight == other.weight

    def __gt__(self, other):
        return self - other > 0

    def __geq__(self, other):
        return self - other >= 0

    @property
    def website(self) -> str:
        if self._website:
            return self._website
        else:
            try:
                issues_url = get_url(self.name, self.date.year,
                                     self.date.month)
                self._website = issues_url
            except ValueError:
                self._website = self.journal_website

        return self._website


class ReadingList(object):

    def __init__(self, cli_args):
        self.record_path = 'reading_record.csv'
        df = publication_info()
        js = [
            extrap_issues(row['name'], row[months], row['wt'], row['Website'])
            for idx, row in df.iterrows()
        ]
        issues = sorted(list(chain(*js)))[::-1]
        self.issue_list = issues
        self.issues = {x.__repr__(): x for x in issues}
        self._make_record()
        self.args = cli_args
        self._selection = pd.DataFrame()

    def get(self, issue_name: str) -> Issue:
        return self.issues[issue_name]

    def mark_read(self, issue_name: str) -> None:
        if issue_name in self.record:
            self.record.at[issue_name] = True
        else:
            raise ValueError
        self.update_record()

    def _make_record(self):
        record = self._to_df()
        try:
            on_disk = pd.read_csv(self.record_path,
                                  index_col=0,
                                  header=None,
                                  squeeze=True)
            record = record.align(on_disk)[0]
            record.update(on_disk)
        except FileNotFoundError:
            pass

        record = record.fillna(False).astype(bool)
        self.record = record
        self.update_record()

    def update_record(self):
        self.record.to_csv(self.record_path)

    def _to_df(self):
        return pd.Series(index=[x for x in self.issues.keys()])

    def __repr__(self):
        return '\n'.join([x.__repr__() for x in list(self.issues.keys())[:10]])

    @property
    def selection(self) -> pd.DataFrame:
        if not self._selection.empty:
            return self._selection
        else:
            rec = self.record
            args = self.args
            # Printing
            if args.read_only:
                df = rec[rec]
            elif args.read:
                df = rec
            else:
                df = rec[~rec]

            if not args.all:
                df = df.head(args.n)

            df = df.reset_index()
            df.index += 1
            self._selection = df

            return self._selection

    def print_selection(self) -> None:
        df = self.selection

        with pd.option_context('display.max_rows', None):
            s_str = str(df)

        s_str = s_str.split('\n', 1)[1]
        if self.args.all:
            s_str = s_str.rsplit('\n', 1)[0]
            less = Less(10)
            s_str | less
        else:
            print(s_str)


class Less(object):

    def __init__(self, num_lines):
        self.num_lines = num_lines

    def __ror__(self, other):

        s = str(other).split("\n")
        for i in range(0, len(s), self.num_lines):
            print(*s[i: i + self.num_lines], sep="\n")
            ans = input("Press <Enter> for more")
            if ans == 'q':
                break


def diff_in_months(a: Union[make_date, datetime],
                   b: Union[make_date, datetime]) -> int:
    yrs = (a.year - b.year) * 12
    mos = a.month - b.month
    return yrs + mos
