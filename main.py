from tkinter  import Tk
from tkinter.filedialog import askopenfilename
from config_reader import getToml
from config_reader import getKeyboardMap
import hotkeyer

# this is an example implementation using the functions from the other files!

# this asks the user for the config file they want to use
filename = askopenfilename(filetypes=[("keyboard config", ".toml")]) # show an "Open" dialog box and return the path to the selected file

# once it has that config, it then converts that file into a toml [str, any] dictionary, then turns that into the KeyboardConfig dataclass, which then gets passed to the hotkeyer to bind the buttons
hotkeyer.mapKeys(getKeyboardMap(getToml(filename)))

# this just prevents the program from immediately stopping and unhooking all of the bindings immediately
while True:
    pass