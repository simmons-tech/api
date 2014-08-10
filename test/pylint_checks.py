import os
import unittest
import sys

#TODO: There are some awkward semantics here.
def for_examples(parameters):
    def decorator(method, parameters=parameters):
        for parameter in parameters:
            def method_for_parameter(self, method=method, parameter=parameter):
                method(self, *parameter)
            name_for_parameter = method.__name__ + "(" + str(parameter) + ")"
            frame = sys._getframe(1)  # pylint: disable-msg=W0212
            frame.f_locals[name_for_parameter] = method_for_parameter
        return None
    return decorator

class WritableObject(object):
    "dummy output stream for pylint"
    def __init__(self):
        self.content = []
    def write(self, st):
        "dummy write"
        self.content.append(st)
    def read(self):
        "dummy read"
        return self.content

def run_pylint(filename):
    "run pylint on the given file"
    from pylint import lint
    from pylint.reporters.text import TextReporter
    ARGS = ["-r","n", "--rcfile=rcpylint"]  # put your own here
    pylint_output = WritableObject()
    lint.Run([filename]+ARGS, reporter=TextReporter(pylint_output), exit=False)
    warnings = []
    for l in pylint_output.read():
	if l.strip() == '':
		continue
	if '*************' in l.strip():
		continue
        warnings.append(l.strip())
    return warnings

class TestLint(unittest.TestCase):
    @for_examples([(x,) for x in os.listdir(os.curdir) if os.path.splitext(x)[1] in ('.py')])
    def test_lint(self, f):
        warnings = run_pylint(f)
        self.assertEqual(len(warnings), 0, "Found " + str(len(warnings)) + " code style errors (and warnings)." + str(warnings))

if __name__ == '__main__':
    unittest.main()

