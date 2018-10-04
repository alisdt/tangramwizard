# tangramwizard

Created by Alisdair Tullo and Catherine Crompton.

Requirements:

* Python 2.7
* Uses "start" (Windows), "play" (Linux), "afplay" (Mac OS X) to play sound.

Usage: In main code directory, `python tw_main.py`

A computerised version of the Barrier Task (Derksen et al., 2014).

The program is designed to describe  a set of 12 tangram tasks to a participant, and instructs them to place the cards in a specific order. Up to four descriptions and provided for each card. The cards are described in a different order over the nine trials. There are two sets of trials each using a different set of 12 tangrams. Synthetic and natural speech descriptions are provided.

Synthetic speech provided by the Festival speech synthesis system by the Centre for Speech Technology Research at the University of Edinburgh ( http://www.cstr.ed.ac.uk/projects/festival/).

Natural speech  recorded in an isolation booth using a Shure SM7 cardioid microphone, and encoded using a Digidesign 003,with sample rate of 16kHz, and a bit depth of 16bi, and the command-line utility Normalize was used to normalise the sound levels across all sound files (http://normalize.nongnu.org/). Output contains the number of turns taken to complete the interaction and time taken to complete the task.

Designed for a PhD project (thesis available at http://hdl.handle.net/1842/25985; articles added as published)
