#!/usr/bin/env bash

###############
# DEFINITIONS #
###############

DIR_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# signal user
function signal {
    osascript ${DIR_PATH}/screen_dim.scpt
    osascript ${DIR_PATH}/screen_brighter.scpt
}


########
# MAIN #
########

signal
python ${DIR_PATH}/anti_people.py
