import argparse
import webbrowser
import sys

from guts import ReadingList, Issue


def main() -> ReadingList:
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


def prompt_ans(rl: ReadingList, prompt: str) -> int:
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
