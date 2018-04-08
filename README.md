# HSautosquelch
Automatically squelch opponent at the beginning of the game.

Dependencies:
Python 3+
Pynput
Pywin32

You need to have logging enabled for hearthstone.
You need to place the script into the folder with the Power.log file, typically in the hearthstone install directory under Logs. For me this is at E:\Hearthstone\Logs\

You should probably create a shortcut to the script so you don't need tp run it from prompt every time. Just right click the script and create shortcut. Make sure that the program for opening .py files is python so that it runs automatically.

The script works best when the game is full screen on the main window, but it will also work most of the time on minimized windows off to the side even, and it doesn't interfere with decktracker etc.

