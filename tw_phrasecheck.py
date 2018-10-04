__author__ = 'atullo2'

from itertools import chain, product
import os
import re

from tw_config import tw_tree_phrases, tw_tangram_phrases, tw_tangram_orders, tw_response_phrases
from tw_flowchart import tw_responses, tw_responses_last
from tw_descriptions import tw_descriptions

# import time assert to stop stray response phrase keys
# (specific to UI, so generalise for audio UI when that is created)
phrase_ids_used = set(x[1] for x in chain(tw_responses.values(),tw_responses_last.values()))
phrase_ids_used -= {""} # excluding empty string, has a special meaning
phrase_ids_defined = set(tw_tree_phrases)
diff = phrase_ids_used ^ phrase_ids_defined
assert not diff

# In config, check descriptions exists for A1-12, B1-12 and no others
all_card_ids = (''.join(x) for x in product(("A", "B"),(str(x) for x in range(1,13))))
assert set(tw_tangram_phrases.keys()) == set(all_card_ids)

# in config, check each order is 1-12
for v in tw_tangram_orders.values():
    assert set(v) == set(range(1,13))

response_keys_expected = set()
for k, v in tw_response_phrases.items():
    if isinstance(v, list):
        for n, _ in enumerate(v):
            response_keys_expected.add(k+"_choice{}".format(n+1))
    else:
        response_keys_expected.add(k)

description_keys_expected = set (tw_descriptions.keys())

def assertpresent(expected, found, subdir, errstr):
    assert not expected - found, errstr+" in {}: {}".format(subdir, str(expected - found))


def check_soundset(subdir):
    description_keys_found = set (x [:-4] for x in os.listdir("sounds/"+subdir) if re.match(r"[AB]\d{1,2}_\d(Y|[TV][FNZ]?)",x))
    assertpresent(description_keys_expected, description_keys_found, subdir, "Missing description sound files ")
    response_keys_found = set (x [:-4] for x in os.listdir("sounds/"+subdir) if not re.match(r"[AB]\d{1,2}_\d(Y|[TV][FNZ]?)",x))
    assertpresent(response_keys_expected, response_keys_found, subdir, "Missing response sound files ")


check_soundset("natural_roger")
check_soundset("natural_catriona")
check_soundset("synth_nick2")
check_soundset("synth_nina")
check_soundset("synth_fiona")