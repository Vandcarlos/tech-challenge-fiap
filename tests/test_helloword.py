import sys
from io import StringIO

import helloworld


def test_hello_world():
    captured_output = StringIO()
    sys.stdout = captured_output
    helloworld.main()
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue() == "Hello, World!\n"
