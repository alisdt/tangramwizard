__author__ = 'atullo2'

from tw_flowchart import tw_responses, tw_responses_last

from tw_config import tw_tangram_orders, tw_tangram_phrases, tw_card_sets

class EndGameException(Exception):
    pass

class TangramGame(object):
    def __init__(self, _ui, _card_set, _trial, _state):
        self.ui = _ui
        self.trial = _trial
        self.tangrams = [None]*12
        card_set = tw_card_sets[int(_card_set)]
        tg_orders = tw_tangram_orders[(int(_card_set),int(_trial))]
        for pos, i in enumerate(tg_orders):
            self.tangrams[pos] = card_set[i-1]
        self.tangram_count = 0
        self.first_description = True
        self.ppt_history = ""
        self.ppt_response = ""
        self.finished = False
        # will be init'd by first_description below
        self.tangram, self.descriptions = None, None
        self.desc_history, self.description = None, None
        self.state = _state
        self.is_exp_turn = True
        self.last_response = None

    def is_mm_response(self, r):
        return all(c in "ABCJKL" for c in r)

    def modifier_hint(self):
        """
        Modifier hint to be used to select the right variant of a shape
        description phrase. Note that this is *only* required to be present
        when desc_response is not empty.
        """
        first_desc = (len(self.descriptions) == 3)
        if self.ppt_response == "X" and not first_desc:
            return "Y" # "Y" always appears on its own
        elif self.trial in [1, 2, 3]:
            modifier = "V"
        else:
            modifier = "T"
        if first_desc:
            # 3 more descriptions left, so current one is first
            if self.tangram_count == 1:
                modifier += "F"
            elif self.tangram_count == 12:
                modifier += "Z"
            else:
                modifier += "N"
        return modifier

    def exp_turn(self):
        try:
            response = self._exp_turn()
            # copy as this is not guaranteed to be unmodified
            self.last_response = response.copy()
            return response
        except EndGameException:
            return self.end_game()

    def _exp_turn(self):
        """Experimenter's turn -- respond to participant"""
        assert self.is_exp_turn
        assert self.ppt_response or self.first_description
        self.is_exp_turn = False
        if self.first_description:
            self.first_description = False
            return self.advance_tg(False)
        if self.ppt_response[0] in "P+-RD" or self.is_mm_response(self.ppt_response):
            return self.do_special()
        if self.ppt_response in "!":
            return self.advance_tg(self.ppt_response == "B")
        if self.ppt_response in "*X":
            return self.advance_desc(self.ppt_response == "S")
        # otherwise, tree lookup
        action, exp_response = self.tree_lookup()
        result = {
            "tangram": self.tangram,
            "ppt_response": "",
            "ppt_history": self.ppt_history,
            "exp_response": "",
            "desc_response": ""
        }
        # do action first
        if action == "TG":
            result = self.advance_tg(False)
        if action == "DESC":
            result = self.advance_desc(False)
        result["exp_response"] = exp_response
        return result

    def ppt_turn(self):
        """Participant's turn -- take input"""
        assert not self.is_exp_turn
        self.is_exp_turn = True
        self.ppt_response = self.ui.ppt_choice()
        self.ppt_history += self.ppt_response
        return {
            "tangram": self.tangram,
            "ppt_history": self.ppt_history,
            "ppt_response": self.ppt_response,
            "exp_response": "",
            "desc_response": ""
        }

    def tree_lookup(self):
        if self.descriptions:
            return tw_responses[self.normalised_responses()]
        else: # last description
            return tw_responses_last[self.normalised_responses()]

    def get_descriptions(self):
        descriptions = tw_tangram_phrases[self.tangram]
        # if there's a stored successful description in state, use that one first
        if self.tangram in self.state:
            successful_description = self.state[self.tangram]
            descriptions.remove(successful_description)
            return [successful_description] + descriptions
        else:
            return descriptions

    def advance_tg(self, is_back):
        if not self.tangrams:
            raise EndGameException
        # if this represents a success, we want to record it in the game state
        # the only such history is a single "Y"
        if self.ppt_history == "Y":
            self.state[self.tangram] = self.description
        self.ppt_history = ""
        self.tangram_count += 1
        self.tangram = self.tangrams.pop(0)
        self.descriptions = self.get_descriptions()
        self.description = self.descriptions.pop(0)
        self.desc_history = [self.description]
        result = {
            "tangram": self.tangram,
            "ppt_history": self.ppt_history,
            "ppt_response": "",
            "exp_response": "",
            "desc_response": self.description,
            "modifier_hint": self.modifier_hint()
        }
        if is_back:
            result["exp_response"] = "sorry_no_going_back"
        return result

    def advance_desc(self, is_skip):
        self.ppt_history = ""
        if self.descriptions:
            self.description = self.descriptions.pop(0)
            self.desc_history.append(self.description)
            result = {
                "tangram": self.tangram,
                "ppt_history": self.ppt_history,
                "ppt_response": "",
                "exp_response": "",
                "desc_response": self.description,
                "modifier_hint": self.modifier_hint()
            }
            if is_skip:
                result["exp_response"] = "sorry_no_skip_desc"
            return result
        else: # special case, no descriptions left, go to next tangram
            result = self.advance_tg(False)
            if is_skip:
                result["exp_response"] = "sorry_no_skip_tg"
            return result

    def end_game(self):
        self.finished = True
        return {
            "tangram": "",
            "ppt_history": "",
            "ppt_response": "",
            "exp_response": "game_over",
            "desc_response": ""
        }

    def normalised_responses(self):
        """Normalise for decision tree"""
        return "".join(x for x in self.ppt_history if x in "YNQ")

    def do_special(self):
        result = {
            "tangram": self.tangram,
            "ppt_response": "",
            "ppt_history": self.ppt_history,
            "exp_response": "",
            "desc_response": ""
        }
        r = self.ppt_response # last response
        if r == "R":
            result = self.last_response
        elif r.startswith("D"):
            if self.desc_history:
                back_idx = int(r[1])
                if back_idx <= len(self.desc_history):
                    result["desc_response"] = self.desc_history[-back_idx]
                    result["modifier_hint"] = self.modifier_hint()
        elif r == "P":
            result["exp_response"] = "tangram_number_{}".format(self.tangram_count)
        elif r == "+":
            result["exp_response"] = "experiment_says_yes"
        elif r == "-":
            result["exp_response"] = "experiment_says_no"
        else:
            # action first, as advance_tg/desc will set exp_response
            # and we want to overwrite it
            if "J" in r:
                result = self.advance_tg(False)
                result["exp_response2"] = "next_shape"
            if "K" in r:
                result = self.advance_desc(False)
                result["exp_response2"] = "another_description"
            if "L" in r:
                if self.descriptions:
                    result = self.advance_desc(False)
                else:
                    result = self.advance_tg(False)
                result["exp_response2"] = "keep_going"
            if "A" in r: result["exp_response"] = "sorry_no_going_back"
            if "B" in r: result["exp_response"] = "sorry_no_skip_desc"
            if "C" in r: result["exp_response"] = "dont_know"
        return result
