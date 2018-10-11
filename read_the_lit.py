import argparse
from itertools import chain
import webbrowser
import sys

import pandas as pd

from config import months
from guts import extrap_issues, Issue


def main():
    args = cli()
    rl = ReadingList(args)
    rl.print_selection()

    if args.open:
        prompt = "Open issue: "
        ans = prompt_ans(rl, prompt)
        issue = rl.get(rl.selection.loc[ans, 'index'])
        open_issue(issue)

    if args.mark_read:
        prompt = "Mark issue as read: "
        ans = prompt_ans(rl, prompt)
        to_be_marked = rl.selection.loc[ans, 'index']
        rl.mark_read(to_be_marked)
        print(f"{to_be_marked} marked as read")

    return rl


def prompt_ans(rl, prompt):
    while True:
        try:
            raw_ans = input(prompt)
            ans = int(raw_ans)
        except ValueError:
            if raw_ans == 'q':
                print("Quit")
                sys.exit(0)
            print("Incorrect issue number.")
            continue

        if ans not in rl.selection.index:
            print("Incorrect issue number.")
            continue

        return ans


class ReadingList(object):

    def __init__(self, cli_args):
        self.record_path = 'reading_record.csv'
        df = pd.read_csv('journal_schedule.csv')
        for month in months:
            df[month] = df[month].fillna(0).replace('X', 1).astype(bool)
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


def open_issue(issue: Issue) -> None:
    webbrowser.open(issue.website, new=1)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', type=int, default=5,
                        help='Number of issues to show.')
    parser.add_argument('--all', '-a', action='store_true',
                        help='Show all issues.')
    parser.add_argument('--read', '-r', action='store_true',
                        help='Also include issues that are already read')
    parser.add_argument('--read-only', action='store_true',
                        help='Only include issues that are already read')
    parser.add_argument('--mark-read', '-m', action='store_true',
                        help='Mark an issue as read.')
    parser.add_argument('--open', '-o', action='store_true',
                        help='Open the website of an issue')
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    rl = main()
