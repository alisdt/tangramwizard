__author__ = 'atullo2'

import re
import sys

def checked_input(prompt, in_constraint, err=None):
    while True:
        text_in = raw_input(prompt)
        if text_in == "exit":
            sys.exit(2)
        if isinstance(in_constraint, list):
            if text_in.upper() in in_constraint:
                return text_in.upper()
            else:
                print("Input must be one of "+", ".join(in_constraint))
        else:
            if re.match(r"\A("+in_constraint+r")\Z", text_in):
                return text_in
            elif err:
                print(err)
