# MVP needed modules:
# reading toml
# reading keyboard

# some method of selecting a toml file

# some function to convert toml file to list of KeyMap(s)

# method which resets keymaps and then sets them based of a list of KeyMap(s)

# something to preform these actions as needed or a loop that calls these methods as needed

from tkinter  import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from config_reader import getToml
from config_reader import getKeyboardMap
import hotkeyer


filename = askopenfilename(filetypes=[("keyboard config", ".toml")]) # show an "Open" dialog box and return the path to the selected file

hotkeyer.mapKeys(getKeyboardMap(getToml(filename)))

while True:
    pass