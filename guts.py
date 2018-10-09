from typing import Union
from dataclasses import dataclass
from datetime import date as make_date, datetime

from config import YEAR0


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


@dataclass(repr=False)
class Issue(object):

    name: str
    date: make_date
    weight: int
    website: str

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


def diff_in_months(a: Union[make_date, datetime],
                   b: Union[make_date, datetime]) -> int:
    yrs = (a.year - b.year) * 12
    mos = a.month - b.month
    return yrs + mos
