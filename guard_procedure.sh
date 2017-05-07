#!/bin/bash

DIR_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

function lock_it {
    # this actually displays screen saver
    /System/Library/Frameworks/ScreenSaver.framework/Resources/ScreenSaverEngine.app/Contents/MacOS/ScreenSaverEngine

    # osascript -e 'tell application "System Events" to keystroke "s" using { command down, control down }'
}
# kill anti_people.py process
kill $(ps aux | grep 'anti_people.py' | awk '{print $2}')

# take picture
source ${DIR_PATH}/take_picture.sh

# lock computer
lock_it
