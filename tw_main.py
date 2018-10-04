__author__ = 'atullo2'

import csv
from datetime import datetime
import json
import os
import sys

# Have to do this so tw_descriptions is ready to import!
if not os.path.exists("tw_descriptions.py"):
    import tw_generate_modified_phrases
    tw_generate_modified_phrases.main()

from tw_game import TangramGame
from tw_textui import TWTextUI

import tw_phrasecheck     # <- this actually runs code to check phrases & ids

STATE_FILENAME = "state.json"

HELLO = """\
Welcome to Tangram Wizard.
Type "exit" at any prompt to exit the application (data may be lost).


"""

PPT_FILE_EXISTS_ERROR = """\
An output file already exists for that participant and trial: {}
The application will now exit.
"""

COLS = (
    "ppt",
    "trial",
    "cards",
    "soundfiles",
    "time",
    "actor",
    "tangram",
    "desc_response",
    "exp_response",
    "exp_response_choice",
    "exp_response2",
    "exp_response2_choice",
    "ppt_response",
    "ppt_history",
)

def start_log(config):
    csv_filename = "tangramwizard_log_ppt{:03d}_{}_trial{:d}.csv".format(
        int(config["ppt"]), config["soundfiles"], int(config["trial"])
    )
    if os.path.exists(os.path.join(".", csv_filename)):
        sys.stderr.write(PPT_FILE_EXISTS_ERROR.format(csv_filename))
        sys.exit(3)
    csv_file = open(csv_filename,"wb")
    out_csv = csv.DictWriter(csv_file, COLS)
    out_csv.writeheader()
    return out_csv

def load_state():
    # if there's an existing game state file, check that ppt and trial match
    if os.path.exists(STATE_FILENAME):
        return json.load(open(STATE_FILENAME, "rb"))
    else:
        return None

def save_state(state):
    if state["trial"] == 9:
        # done with this participant, delete existing state file
        os.remove(STATE_FILENAME)
        return
    json.dump(
        state,
        open(STATE_FILENAME, "wb"),
        sort_keys=True,
        indent=4,
        separators=(',', ': ')
    )

def config_from_state(c):
    return {
        k: v
        for k, v in c.items()
        if k in ("ppt", "trial", "cards", "soundfiles")
    }

def sayit(ui, exp_response, config):
    # create a dummy "turn" and run this to say something
    # used for intros
    intro = {
        "tangram": "",
        "ppt_history": "",
        "ppt_response": "",
        "exp_response": exp_response,
        "exp_response2": "",
        "desc_response": ""
    }
    intro.update(config)
    ui.show_turn(intro, {})

def trial1_intro_natural(ui, config):
    ui.pause("Press ENTER to say the first intro phrase.")
    sayit(ui, "start_intro_natural_1", config)
    ui.pause("Press ENTER to say the second intro phrase.")
    sayit(ui, "start_intro_natural_2", config)


def nexttrial_intro_natural(ui, config):
    ui.pause("Press ENTER to say the trial intro phrase.")
    sayit(ui, "trial_intro_natural", config)

def trial1_intro_synth(ui, config):
    ui.pause("Press ENTER to say the intro phrase.")
    sayit(ui, "start_intro_synth", config)

def nexttrial_intro_synth(ui, config):
    ui.pause("Press ENTER to say the trial intro phrase.")
    sayit(ui, "trial_intro_synth", config)

def do_intro(ui, config):
    intro_funcs = {
        (True, True): trial1_intro_synth,
        (True, False): trial1_intro_natural,
        (False, True): nexttrial_intro_synth,
        (False, False): nexttrial_intro_natural
    }
    first_trial = (config["trial"] == 1)
    is_synth = config["soundfiles"].lower().startswith("synth")
    intro_funcs[(first_trial,is_synth)](ui, config)

def run(ui, log=True):
    ui.show(HELLO)
    state = load_state()
    if state is None:
        config = ui.config()
        state = config.copy() # will also hold prev. successful descriptions
        state["trial"] = 0
    state["trial"] += 1
    config = config_from_state(state)

    if log:
        out_csv = start_log(config)

    do_intro(ui, config)

    ui.pause("Press ENTER to start the timer and continue.")
    time_start = datetime.now()
    game = TangramGame(ui, config["cards"], config["trial"], state)
    is_exp_turn = True
    while not game.finished:
        if is_exp_turn:
            turn, actor = game.exp_turn(), "D"
        else:
            turn, actor = game.ppt_turn(), "P"
        if "exp_response2" not in turn:
            turn["exp_response2"] = ""

        turn.update(config)
        turn["time"] = (datetime.now() - time_start).total_seconds()
        turn["actor"] = actor
        ui.show_turn(turn, state)
        if log:
            out_csv.writerow(turn)
        is_exp_turn = not is_exp_turn
    save_state(state)

if __name__ == "__main__":
    ui = TWTextUI(verbose=False)
    run(ui)
