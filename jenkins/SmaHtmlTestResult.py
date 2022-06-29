import traceback
import sys

from HtmlTestRunner.result import HtmlTestResult


# We override the _exc_info_to_string to fix the following bug in the library
# AttributeError: 'HtmlTestResult' object has no attribute '_count_relevant_tb_levels'. Did you mean: '_is_relevant_tb_level'?
# If an assertion is false
class SmaHtmlTestResult(HtmlTestResult):
    def _exc_info_to_string(self, err, test):
        """ Converts a sys.exc_info()-style tuple of values into a string."""
        # if six.PY3:
        #     # It works fine in python 3
        #     try:
        #         return super(_HTMLTestResult, self)._exc_info_to_string(
        #             err, test)
        #     except AttributeError:
        #         # We keep going using the legacy python <= 2 way
        #         pass

        # This comes directly from python2 unittest
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        msg_lines = traceback.format_exception(exctype, value, tb)

        if self.buffer:
            # Only try to get sys.stderr as it might not be
            # StringIO yet, e.g. when test fails during __call__
            try:
                error = sys.stderr.getvalue()
            except AttributeError:
                error = None
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msg_lines.append(error)
        # This is the extra magic to make sure all lines are str
        encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        lines = []
        for line in msg_lines:
            if not isinstance(line, str):
                # utf8 shouldn't be hard-coded, but not sure f
                line = line.encode(encoding)
            lines.append(line)

        return ''.join(lines)
