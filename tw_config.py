__author__ = 'atullo2'

tw_tree_phrases = {
    "not_sure_other_desc": [
        "I'm not sure, would you like a different description?",
        "I'm not sure, I can describe it differently if you like?",
        "I'm not sure, shall I describe it in a different way?",
        "I dont know, would a different description help?"
    ],
    "only_have_desc": [
        "I only have the descriptions, not the cards. Would you like another description?",
        "I don't have the shapes here, I only have the descriptions. I can give you another description?",
        "I can't see the cards, I only have the descriptions here. Shall I give you a different description?",
        "I'm not able to see the cards, I only have the descriptions. Shall I read you a different description?",
        "All I can see are the descriptions, not the shapes on the cards. Would you like me to give an alternative description?"
    ],
    "move_on_shape": [
        "Let's try the next shape",
        "Let's try the next card"

    ]
}



# Maybe these should go in text UI (could be reused for festival speech UI?)
tw_additional_response_phrases = {
    "start_intro_natural_1": "Hello, can you hear me?",
    "start_intro_natural_2": (
        "Great. I'm David. I'm going to be describing these shapes to you today"
        +" and telling you what order to put them in. Are you ready to start?"
    ),
    "start_intro_natural_3": "Great. I'm David. I'm going to be describing these shapes to you today"
        +" and telling you what order to put them in. Are you ready to start?",

    "trial_intro_natural": ["Ready to start the next one?", "Are you ready to go?"],
    "start_intro_synth": "Are you ready to begin?",
    "trial_intro_synth": "Are you ready to start the next trial?",
    "experiment_says_yes": ["Yes.","Yes.","Yes.","Yes.",],
    "experiment_says_no": ["No.","No.","No.","No.","No.",],
    "sorry_no_going_back":[
        "I'm sorry but the rules are that we can't go back to change a card.",
        "According to the rules, we can't go back to change cards.",
        "I'm sorry, the rules say that we can't change previous cards"
    ],
    # For the split commands
    # We arent allowed to skip a shape x 3
    "sorry_no_skip_desc": [
        "We aren't allowed to skip a shape.",
        "The rules say that we can't skip a card",
        "We're not supposed to miss out any of the cards"
    ],
    # We can't go back to change a card
    "sorry_no_skip_tg": [
        "We aren't allowed to go back and change a shape.",
        "Sorry, the rules are that we can't go back and change a card.",
        "We're not supposed to go back to a card after we've gone past it."
    ],
    # Don't know
    "dont_know": "I don't know",
    #Shall I give you another description?",Shall we move on to the next shape?
    "keep_going": [
        "Lets keep going.",
        "Lets carry on.",
        "Let us move on."
    ],
    "next_shape": [
        "Lets try the next shape.",
        "Lets try the next card.",
        "Let us move on to the next card"
    ],
    "another_description": [
        "I'll give you another description.",
        "I'll try describing it in a different way.",
        "I'll describe it in a different way."
    ],
    "game_over": [
        "That's it, looks like the game is finished.",
        "We're finished"
    ],
}

tw_theory_of_mind_phrases = ["only_have_desc", "only_have_shape"]

numbers = (
    "one", "two", "three", "four",
    "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve"
)

for n, x in enumerate(numbers):
    tw_additional_response_phrases["tangram_number_{}".format(n+1)] = "We're on card number, {}.".format(x)

tw_response_phrases = tw_tree_phrases.copy()
tw_response_phrases.update(tw_additional_response_phrases)

# tangram id -> (dict of phrase id -> phrase)
tw_tangram_phrases = {
# Set A, Cards 1-12, description presentation order 4-1
# Set A includes A1,A4,A5,A7,A9,A12,B1,B3,B5,B7,B10,B11
"A1":   ["A1_4", "A1_3", "A1_2", "A1_1"], #1.1
"A4":   ["A4_4", "A4_3", "A4_2", "A4_1"], #1.2
"A5":   ["A5_4", "A5_3", "A5_2", "A5_1"], #1.3
"A7":   ["A7_4", "A7_3", "A7_2", "A7_1"], #1.4
"A9":   ["A9_4", "A9_3", "A9_2", "A9_1"], #1.5
"A12":  ["A12_4", "A12_3", "A12_2", "A12_1"], #1.6
"B1":   ["B1_4", "B1_3", "B1_2", "B1_1"], #1.7
"B3":   ["B3_4", "B3_3", "B3_2", "B3_1"], #1.8
"B5":   ["B5_4", "B5_3", "B5_2", "B5_1"], #1.9
"B7":   ["B7_4", "B7_3", "B7_2", "B7_1"], #1.10
"B10":  ["B10_4", "B10_3", "B10_2", "B10_1"], #1.11
"B11":  ["B11_4", "B11_3", "B11_2", "B11_1"], #1.12
# Set B, Cards 1-12, description presentation order 4-1
# Set B includes A2,A3,A6,A8,A10,A11,B2,B4,B6,B8,B9,B12
"A2":   ["A2_4", "A2_3", "A2_2", "A2_1"], #2.1
"A3":   ["A3_4", "A3_3", "A3_2", "A3_1"],#2.2
"A6":   ["A6_4", "A6_3", "A6_2", "A6_1"],#2.3
"A8":   ["A8_4", "A8_3", "A8_2", "A8_1"],#2.4
"A10":  ["A10_4", "A10_3", "A10_2", "A10_1"], #2.5
"A11":  ["A11_4", "A11_3", "A11_2", "A11_1"], #2.6
"B2":   ["B2_4", "B2_3", "B2_2", "B2_1"], #2.7
"B4":   ["B4_4", "B4_3", "B4_2", "B4_1"], #2.8
"B6":   ["B6_4", "B6_3", "B6_2", "B6_1"], #2.9
"B8":   ["B8_4", "B8_3", "B8_2", "B8_1"], #2.10
"B9":   ["B9_4", "B9_3", "B9_2", "B9_1"], #2.11
"B12":  ["B12_4", "B12_3", "B12_2", "B12_1"] #2.12

}

# map (card set, trial) -> list of tangram order
tw_tangram_orders = {
    #Here is where the pseudo random orderings go. ("card set"2, trial number)
    #
    (1, 1): [1,7,3,10,5,11,12,2,9,4,8,6], # E/H/E/H/E/H/E/H/E/H/E/H
    (1, 2): [5,7,1,11,8,6,3,10,9,4,12,2], # E/H/E/H/E/H/E/H/E/H/E/H
    (1, 3): [3,11,9,2,5,10,1,7,12,6,8,4], # E/H/E/H/E/H/E/H/E/H/E/H
    (1, 4): [12,1,4,5,6,3,7,10,8,9,11,2], # Random
    (1, 5): [3,9,6,11,1,4,8,7,10,12,2,5], # Random
    (1, 6): [8,10,1,6,3,7,5,4,9,12,2,11], # Random
    (1, 7): [7,11,3,10,5,9,1,4,12,8,2,6], # Random
    (1, 8): [4,9,12,3,11,6,5,10,7,2,8,1], # Random
    (1, 9): [9,12,11,4,2,5,10,1,7,8,3,6], # Random

    (2, 1): [2,12,4,1,5,9,7,3,8,6,11,10], # E/H/E/H/E/H/E/H/E/H/E/H
    (2, 2): [7,9,11,6,2,1,5,8,12,4,3,10], # E/H/E/H/E/H/E/H/E/H/E/H
    (2, 3): [8,1,11,10,5,3,7,12,4,9,2,6], # E/H/E/H/E/H/E/H/E/H/E/H
    (2, 4): [3,9,5,2,7,12,8,4,11,6,10,1], # Random
    (2, 5): [12,8,2,7,5,3,10,9,4,11,6,1], # Random
    (2, 6): [4,11,3,9,6,12,8,2,1,5,10,7], # Random
    (2, 7): [7,1,5,9,6,3,11,8,10,4,12,2], # Random
    (2, 8): [8,4,5,6,7,11,3,12,1,2,10,9], # Random
    (2, 9): [10,4,12,11,3,2,6,1,5,9,7,8]  # Random
}

tw_card_sets = {
    1: ["A1","A4","A5","A7","A9","A12","B1","B3","B5","B7","B10","B11"],
    2: ["A2","A3","A6","A8","A10","A11","B2","B4","B6","B8","B9","B12"]
}
