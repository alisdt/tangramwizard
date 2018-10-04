__author__ = 'atullo2'

# From Korin Richmond (CSTR):
#
# Sure, no problem - if you just need straight synthesis of 900 sentences, the easiest for you would probably just be to use the CGI interface directly.
#
# In other words, a script (e.g. python) which accesses
#
# http://www.cstr.ed.ac.uk/cgi-bin/cstr/festivalspeak.cgi
#
# directly.  The fields you need to set in your POST request would be:
#
# voice (=nick2)
# UserText (= the text to synthesise)

# OK. I've added a flag to the cgi script to specify no filtering
# In your request to the cgi, just set an additional field "FilterSwearWords" to "off", and you'll be able to freely
# synthesise whatever you like ;)


import sys
sys.path.append("..")

from os.path import join, exists
import time
import urllib as ul
import urllib2 as ul2

from tw_config import tw_response_phrases
try:
    from tw_descriptions import tw_descriptions
except:
    sys.stderr.write("Unable to find tw_descriptions, if it does not exist please run tw_generate_modified_phrases.\n")
    sys.exit(-1)

FESTIVALSPEAK_URL = "http://www.cstr.ed.ac.uk/cgi-bin/cstr/festivalspeak.cgi"
OUT_PATH = "/Users/s0675382/Desktop/tangramwizard/code/sounds/synth_nina"
COURTESY_DELAY = 2.0 # delay in seconds, to avoid overloading the server

def festivalspeak_get(text):
    text = text.replace("tangram", "shape")
    post_data = ul.urlencode({'voice': 'nina', 'UserText': text, 'FilterSwearWords': 'off'})
    req = ul2.urlopen(FESTIVALSPEAK_URL, post_data)
    return req.read()

def festival_to_file(text, filename):
    if not exists(out_filename):
        wav_data = festivalspeak_get(text)
        open(filename,"w").write(wav_data)
        time.sleep(COURTESY_DELAY)

for desc_id, desc_text in tw_descriptions.items():
    out_filename = join(OUT_PATH, desc_id+".wav")
    festival_to_file(desc_text, out_filename)

for exp_id, exp_text in tw_response_phrases.items():
    if type(exp_text) == type([]):
        choices = range(1,len(exp_text)+1)
        for choice in choices:
            out_filename = join(OUT_PATH, exp_id+"_choice{}.wav".format(choice))
            festival_to_file(exp_text[choice-1], out_filename)
    else:
        out_filename = join(OUT_PATH, exp_id+".wav")
        festival_to_file(exp_text, out_filename)