import os
import random

from aqt import mw
from aqt.qt import *
from anki.hooks import wrap
from anki.sound import play

from os import listdir
from os.path import isfile, join

# gets the 'birl' directory and all files inside
file_dir = os.path.join(mw.pm.addonFolder(), 'birl-reinforcement')
all_files = [a for a in [f for f in listdir(file_dir) if isfile(join(file_dir, f))] if a[-4:] == ".mp3"]

# dif is the distance of the reinforcement
# spread is the maximum spread around dif
mw.birl = {
	"times": 0,
	"next": 0,
	"spread": 5,
	"dif": 20,
}

# plays a random mp3 file in the 'birl' folder
def birl():
	sound = all_files[random.randint(0, len(all_files)-1)]
	play(file_dir + '/' + sound)

# gets time of the next reinforcement
def get_next():
	mw.birl["next"] = mw.birl["times"] + max(1, mw.birl["dif"] + random.randint(-mw.birl["spread"], mw.birl["spread"]));

# check if reinforcement is due
def maybe_birl():
    if mw.birl["times"] == mw.birl["next"]:
		birl()
		get_next()
    mw.birl["times"] += 1

# calls maybe_birl on every card shown
mw.reviewer.nextCard = wrap(mw.reviewer.nextCard, maybe_birl)
