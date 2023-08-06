from argparse import ArgumentParser
import os
import pdb
import sys

from dep_appearances.appearances_report import AppearancesReport

def main():
    parser = ArgumentParser(description='Find dependencies that are unused and underused in your codebase.')

    parser.add_argument(
        'project_root',
        metavar='PATH',
        type=str,
        nargs='?',
        default=os.getcwd(),
        help="The path to your project's root (defaults to your current working directory)"
    )

    parser.add_argument(
        '--underused_threshold',
        type=int,
        default=2,
        help='The threshold to set for marking dependencies as underused (default: 2)'
    )

    args = parser.parse_args()

    report = AppearancesReport(project_root=args.project_root).compile()
    unused_dependencies = report.unused_dependencies()
    underused_dependencies = report.underused_dependencies(usage_threshold=args.underused_threshold)

    if len(unused_dependencies) == 0:
        print("No unused dependencies found")
    else:
        print("Unused dependencies:")
        for dep in unused_dependencies:
            print(f"\t{dep.name}")

    print("")

    if len(underused_dependencies) == 0:
        print("No underused dependencies found")
    else:
        print(f"Underused dependencies (usage threshold = {args.underused_threshold}):")
        for dep in underused_dependencies:
            print(f"\t{dep.name}\n\t\timported in:")

            for import_statement in dep.import_statements:
                print(f"\t\t{os.path.relpath(import_statement.source_file)}:{import_statement.line_number}")

            print("")

if __name__ == "__main__":
    main()
