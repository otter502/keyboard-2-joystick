from tkinter  import Tk
from tkinter.filedialog import askopenfilename
from config_reader import getToml
from config_reader import getKeyboardMap
import hotkeyer


filename = askopenfilename(filetypes=[("keyboard config", ".toml")]) # show an "Open" dialog box and return the path to the selected file

hotkeyer.mapKeys(getKeyboardMap(getToml(filename)))

while True:
    pass