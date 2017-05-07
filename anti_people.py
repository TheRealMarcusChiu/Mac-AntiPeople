import os  # needed for exec command
import sys
import select
import termios
from threading import Thread
from pykeyboard import PyKeyboardEvent
from pymouse import PyMouseEvent

###############
# DEFINITIONS #
###############


class Event:
    def __init__(self, string):
        self.string = str(string)
        pass

    def execute(self):
        exec self.string


class MouseEvent(PyMouseEvent):
    def __init__(self, left_click_event, right_click_event):
        self.left_click_event = left_click_event
        self.right_click_event = right_click_event
        PyMouseEvent.__init__(self)

    def click(self, x, y, button, press):
        if button == 1:  # left
            if press == 1:
                self.left_click_event.execute()
        if button == 2:  # right
            if press == 1:
                self.right_click_event.execute()

    def move(self, x, y):
        # print 'event: click, x: {}, y: {}'.format(x, y)
        pass


# does not work yet
class KeyEvent(PyKeyboardEvent):
    def __init__(self):
        PyKeyboardEvent.__init__(self)

    def tap(self, keycode, character, press):
        print 'keycode      : ' + str(keycode)
        print 'character    : ' + str(character)
        print 'press        : ' + str(press)
        print 'event: tab, keycode: {}, character: {}'.format(keycode, character)


# this is a substitute for KeyEvent class
class KeyEvent1(Thread):
    def __init__(self, key, key_clicked_event, other_key_clicked_event):
        self.key = key
        self.key_clicked_event = key_clicked_event
        self.other_key_clicked_event = other_key_clicked_event
        super(KeyEvent1, self).__init__()

    def run(self):
        with KeyPoller() as keyPoller:
            while True:
                key = keyPoller.poll()
                if key is not None:
                    if key == self.key:
                        self.key_clicked_event.execute()
                    else:
                        self.other_key_clicked_event.execute()


class KeyPoller:
    def __init__(self):
        self.curEventLength = 0
        pass

    def __enter__(self):
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    @staticmethod
    def poll():
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if not dr == []:
            return sys.stdin.read(1)
        return None


########
# MAIN #
########

dir_path = os.path.dirname(os.path.abspath(__file__))

script_stop = dir_path + '/stop.sh'
script_guard = dir_path + '/guard_procedure.sh'

command_stop = "os.system('" + script_stop + "')"
command_guard = "os.system('" + script_guard + "')"

event_stop = Event(command_stop)  # was "os.system('kill %d' % os.getpid())"
event_guard = Event(command_guard)

m = MouseEvent(event_guard, event_guard)
k = KeyEvent1("q", event_stop, event_guard)

m.start()
k.start()

m.join()
k.join()
