import os
import sys
from UI import UserInterface
from FileHandling import FileHandler
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019


def main(path=None):
    """
    main loop
    """
    if len(sys.argv) > 1:
        path = sys.argv[-1]
    if path is not None:
        filehandler = FileHandler(path)
    else:
        filehandler = FileHandler()
    mainui = UserInterface(filehandler=filehandler)


if os.name == "nt":
    path = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
else:
    path = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"

if __name__ == '__main__':
    main(path)
