__author__ = 'atullo2'

# Responses for all descriptions except last
tw_responses = {
    "Y":    ("TG",     ""),
    "N":    ("DESC",   ""),
    "Q":    ("",     "not_sure_other_desc"),
    "QY":   ("DESC", ""),
    "QN":   ("TG",   "move_on_shape"),
    "QQ":   ("",     "only_have_desc"),
    "QQY":  ("DESC", ""),
    "QQN":  ("TG",   "move_on_shape"),
    "QQQ":  ("",     "only_have_desc"),
    "QQQY": ("DESC", ""),
    "QQQN": ("TG",   "move_on_shape"),
    "QQQQ": ("TG",   "move_on_shape")
}

# Responses for last description
# Responses for last description
tw_responses_last = {
    "Y":   ("TG", ""),
    "N":   ("TG", "move_on_shape"),
    "Q":   ("TG", "move_on_shape")
}