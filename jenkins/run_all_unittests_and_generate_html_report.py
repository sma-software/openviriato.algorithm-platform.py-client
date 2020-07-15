import unittest
from HtmlTestRunner import HTMLTestRunner
import sys


def main():
    if len(sys.argv) != 4:
        print('Expected arguments: [discover_path_for_unittests] [report_output_path] [report_name]', file=sys.stderr)
        sys.exit(1)

    discover_path = sys.argv[1]
    output_path = sys.argv[2]
    report_name = sys.argv[3]

    test_suite = unittest.TestLoader().discover(start_dir=discover_path)
    html_test_runner = HTMLTestRunner(
        output=output_path,
        combine_reports=True,
        report_name=report_name,
        open_in_browser=False,
        add_timestamp=False,
        verbosity=3)
    html_test_runner.run(test_suite)
    sys.exit(0)


if __name__ == '__main__':
    main()
