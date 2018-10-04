__author__ = 'atullo2'

import random

def TWAutoRunTreeUI(object):
    def config(self):
        return {
           "ppt": "0",
            "cards": "1",
            "soundfiles": "1"
        }

    def pause(self, msg):
        pass

    def ppt_choice(self):
        #return curr_response_tree.pop(0)
        pass

    # phrases: numerical id -> phrase
    # phrase_ids: list of numerical ids
    def exp_phrase_choice(self, phrases, phrase_ids):
        return random.choice(phrase_ids)

    def show_turn(self, turn):
        # if we've changed descriptions, go to next tree
        pass

    def show(self, txt):
        pass