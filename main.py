import os
import sys
from UI import UserInterface
from FileHandling import FileHandler
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019


def main():
    if len(sys.argv) > 1:
        path = sys.argv[-1]
    else:
        if os.name == "nt":
            path = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
        else:
            path = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"

    filehandler = FileHandler()
    if os.path.isfile(path):
        mainui = UserInterface(filehandler=filehandler, path=path)
    else:
        mainui = UserInterface(filehandler=filehandler)

if __name__ == '__main__':
    main()
