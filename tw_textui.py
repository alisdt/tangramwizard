__author__ = 'atullo2'

import platform
from os.path import join
import os
import pprint
import random
import subprocess

from tw_config import tw_response_phrases
from tw_descriptions import tw_descriptions
from tw_util import checked_input

if platform.system() == "Windows":
    PLAY_SOUND_CMD = "start"
elif platform.system() == "Linux":
    PLAY_SOUND_CMD = "play"
elif platform.system() == "Darwin":
    PLAY_SOUND_CMD = "afplay"
else:
    assert False, "Unrecognised operating system: "+platform.system()

class TWTextUI(object):
    def __init__(self, verbose=True):
        self.verbose = verbose

    FMT = """\
Participant sees tangram: {tangram}
Participant's response history: {ppt_history}
Participant's response: {ppt_response}
Experiment response: {exp_response_out}
Experiment response chosen: {exp_response_choice}
Experiment response 2: {exp_response2_out}
Experiment response 2 chosen: {exp_response2_choice}
Experiment description phrase: {desc_response_out}
"""

    PPT_CHOICE_DOC = """\
Tree-advancing choices:
 Y : Participant has replied "yes"
 N : Participant has replied "no"
 Q : Participant has asked a question
 X : Participant has asked directly for the next description

Simple answers for participant questions:
 P : Participant has asked for current tangram number (i.e. tangram number will be given)
 + : Participant has asked a question with answer "yes" (i.e. response "yes" will be given)
 - : Participant has asked a question with answer "no" (i.e. response "no" will be given)

Special actions:
 ! : Advance to next tangram, just giving the first description
 * : Advance to next description
 R : Participant has asked for a repeat of last response (description or other response)
 D1 : Participant has asked for a repeat of last description they got for this tangram (D2 for second last etc.)
 M : Mix-and-match response -- will be explained interactively
"""

    MM_TEXT_PART1_CHOICE = """\
A) I'm sorry, but the rules are that we can't go back and change a card
B) We aren't allowed to skip a card
C) I don't know
Enter) No response
"""

    MM_TEXT_PART2_CHOICE = """\
J) Let's move on to the next card (action: go to next tangram)
K) I'll give you another description (action: go to next description)
L) Let's continue (action: go to next tangram or description, as appropriate)
Enter) No action
"""

    SOUNDFILE_SETS = ["SYNTH_NICK2", "SYNTH_FIONA", "NATURAL_ROGER", "NATURAL_CATRIONA", "SYNTH_NINA"]

    def config(self):
        self.show("Starting new run")
        ppt = checked_input("Participant number:", r"\d+", "Input must be a number.")
        cards = checked_input("Card set:", ["1", "2"])
        soundfiles = checked_input("Sound file set:", self.SOUNDFILE_SETS)
        return {
            "ppt": int(ppt),
            "cards": int(cards),
            "soundfiles": soundfiles.upper()
        }

    def print_config(self, c):
        self.show(pprint.pformat(c))

    def pause(self, msg):
        _ = raw_input(msg)

    def get_mix_and_match(self):
        part1 = checked_input(
            "Choose one of the following responses: \n"+self.MM_TEXT_PART1_CHOICE,
            ["A", "B", "C", ""]
        )
        part2 = checked_input(
            "Choose one of the following responses (with action): \n"+self.MM_TEXT_PART2_CHOICE,
            ["J", "K", "L", ""]
        )
        return part1+part2

    def ppt_choice(self):
        ppt_input_text = "Y/N/Q/X/P/+/-/*/!/R/D(1234)/M"
        ppt_input_re = r"[YNQXP+\-*!?RM]|D[1234]"
        while True:
            prompt = "What was the participant's response ({}, ? for help):".format(ppt_input_text)
            ppt_response = checked_input(prompt, ppt_input_re)
            if ppt_response == "?":
                self.show(self.PPT_CHOICE_DOC)
            elif ppt_response == "M":
                return self.get_mix_and_match()
            else:
                return ppt_response

    def randomise_exp_choice(self, turn, idx, state):
        choice_idx = idx+"_choice"
        out_idx = idx+"_out"
        if turn[idx]:
            turn[choice_idx], turn[out_idx] = self.exp_response_randomise(turn[idx], state)
        else:
            turn[choice_idx], turn[out_idx] = 0, ""


    def show_turn(self, turn, state):
        # change exp_response and phrase_response fields to human-readable responses, if present
        modhint = ""
        self.randomise_exp_choice(turn, "exp_response", state)
        self.randomise_exp_choice(turn, "exp_response2", state)
        if turn["desc_response"]:
            turn["desc_response_out"] = tw_descriptions[turn["desc_response"]+turn["modifier_hint"]]
            modhint = turn["modifier_hint"]
            del turn["modifier_hint"]
        else:
            turn["desc_response_out"] = ""
        # print text
        self.show(self.FMT.format(**turn))
        # play sound
        # very occasionally there's an experiment response and description, if so play both
        to_play = [
            (r, c, m)
            for r, c, m
            in [
                (turn["exp_response"], turn["exp_response_choice"], ""),
                (turn["exp_response2"], turn["exp_response2_choice"], ""),
                (turn["desc_response"], 0, modhint)
            ]
            if r != ""
        ]
        for response, choice, modhint in to_play:
            self.play(turn["soundfiles"], response, modhint, choice)
        del turn["desc_response_out"]
        del turn["exp_response_out"]
        del turn["exp_response2_out"]

    def exp_response_randomise(self, exp_response, state):
        r = tw_response_phrases[exp_response]
        if type(r) == type(''):
            return 0, r
        else:
            if exp_response in state:
                idx = state[exp_response]
                while idx == state[exp_response]:
                    idx = random.randrange(len(r))
            else:
                idx = random.randrange(len(r))
            state[exp_response] = idx
            return idx+1, r[idx]

    def show(self, txt):
        print(txt)

    def play(self, sound_set, sound_id, modhint, sound_choice):
        self.show("Playing sound {}/{} from {} with {}".format(
            sound_id, sound_choice, sound_set, PLAY_SOUND_CMD)
        )
        if sound_choice == 0:
            sound_filename = "{}{}.wav".format(sound_id, modhint)
        else:
            sound_filename = "{}_choice{}.wav".format(sound_id, sound_choice)
        sound_pathname = join("sounds", sound_set.lower(), sound_filename)
        devnull = open(os.devnull, "w")
        subprocess.call([PLAY_SOUND_CMD, sound_pathname], stdout=devnull, stderr=devnull)
        devnull.close()