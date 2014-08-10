import unittest
import pep8
import os
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

def pep8test():
    # TODO: Do something...
    def decorator(method):
        print "Would be splitting into pep8 subtests here."
        method()
    return decorator


class TestCodeFormat(unittest.TestCase):
    @for_examples([(x,) for x in os.listdir(os.curdir) if os.path.splitext(x)[1] in ('.py')])
    def test_pep8_conformance(self, f):
        #Test that we conform to PEP8.
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([f])
        for thing in result.get_statistics(prefix=''):
            print f, thing
        self.assertEqual(result.total_errors, 0, "Found " + str(result.total_errors) + " code style errors (and warnings).")


if __name__ == '__main__':
    unittest.main()
