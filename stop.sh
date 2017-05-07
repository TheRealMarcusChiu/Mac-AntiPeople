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

kill $(ps aux | grep 'anti_people.py' | awk '{print $2}')
signal
