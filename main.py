from shutil import copyfile
from datetime import datetime
import os
from tkinter import *
from tkinter import ttk
import sys

# Encoding stuff : https://www.devdungeon.com/content/working-binary-data-python
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019

# sharp fonts in high res (https://stackoverflow.com/questions/41315873/
# attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
if os.name == "nt":
    from ctypes import windll, pointer, wintypes
    fpath = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass  # this will fail on Windows Server and maybe early Windows
else:
    fpath = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"



# filepaths
# fpath = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"
# fpath = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
fpath = fpath.replace("\\", "/")
folder = "/".join(fpath.split("/")[:-1])

filename = fpath.split("/")[-1]
bkfolder = folder + "/KNOTE_backups"

# overrules premade filepath with cmd prompt input.
args = sys.argv
if len(sys.argv) > 1:
    fpath = sys.argv[-1]

class UserInterface():

    _names = {}

    def __init__(self, name = None):
        if id != None:
            self._name_ = id
        else:
            self._name_ = "n_" + str(len(self._names))
        print("initiated userinterface {}".format(self._name_))
        self.itemlist = []
        self.root = Tk()
        self.previeweditem = ""

        self.pw = PanedWindow(self.root, orient=HORIZONTAL)
        self.pw.pack(fill=BOTH, expand=1)

        self.pane_left = Frame(self.root)
        self.pw.add(self.pane_left)

        self.pane_right = Frame(self.root)

        self.pw.add(self.pane_right)

        self.frame_left = Frame(self.pane_left)
        self.frame_left.pack(fill=BOTH, expand=1)
        self.frame_center = Frame(self.pane_right)
        self.frame_center.grid(row=0, column=0, sticky=W+N, rowspan=4)
        self.frame_right = Frame(self.pane_right, borderwidth=5,
                relief="solid")
        self.frame_right.grid(row=0, column=1, sticky=W+E+N+S)
        self.sf1 = Text(self.frame_left, height=1, width=12, borderwidth=2,
                relief="solid", highlightthickness=0)
        self.sf1.grid(row=0, column=0)
        self.sb1 = Button(self.frame_left, text="SAVEFILE", width=10)
        self.sb1.grid(row=0, column=1)
        self.sb1.bind("<ButtonRelease-1>", self.savefile)
        self.sb2 = Button(self.frame_left, text="X", width=3)
        self.sb2.grid(row=0, column=2)

        # Setup treebar and scroll
        self.l1 = ttk.Treeview(self.frame_left)
        self.yscroll = Scrollbar(self.frame_left, orient=VERTICAL)
        self.yscroll.config(width=10)
        self.l1['yscrollcommand'] = self.yscroll.set
        self.yscroll['command'] = self.l1.yview
        self.l1.grid(row=1, column=0, columnspan=3,  padx=(30),
                pady=(10), sticky=N+S+E+W)
        self.yscroll.grid(row=1, column=0, columnspan=3, sticky=N+S+E)
        self.l1.bind("<ButtonRelease-1>", self.changeselection)

        self.frame_left.rowconfigure(1, weight=1)
        self.frame_left.columnconfigure(0, weight=1)
        self.frame_left.columnconfigure(1, weight=1)

        self.vbs = []  # Vertical bar
        middlebuttons = ("Up","Down", "<-", "New", "New Sub", "Delete",
        "Rename", "Parent")
        for a, button_text in enumerate(middlebuttons):
            self.vbs.append(Button(self.frame_center, text=button_text))
            self.vbs[a].pack(fill=BOTH)
            # vbs[a].grid(row=int(a)+1)

        # label
        self.tx1 = Label(self.frame_right, text="Preview")
        self.tx1.grid(row=0, column=0, columnspan=3)
        self.tx2 = Label(self.frame_right, text="Editing")
        self.tx2.grid(row=2, column=0)

        self.e1 = Text(self.frame_right, fg="#555", font=("Courier", 15),
                  padx=10, pady=10, highlightthickness=0,
                  borderwidth=1, relief="solid")
        self.e1.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W)

        self.e2 = Text(self.frame_right, font=("Courier", 15), borderwidth=3,
                  relief="solid", padx=10, pady=10, highlightthickness=0)
        self.e2.grid(row=3, column=0, columnspan=3, sticky=N+S+E+W)

        self.vb1 = Button(self.frame_right, text="Edit")
        self.vb1.grid(row=2, column=1)
        self.vb1.bind("<ButtonRelease-1>", self.edititem)
        self.vb2 = Button(self.frame_right, text="Save")
        self.vb2.grid(row=2, column=2)
        self.vb2.bind("<ButtonRelease-1>", self.saveitem)

        self.frame_right.rowconfigure(0, weight=1)
        self.frame_right.rowconfigure(1, weight=2)
        self.frame_right.rowconfigure(2, weight=1)
        self.frame_right.rowconfigure(3, weight=1)
        self.frame_right.columnconfigure(1, weight=1)

        """
        Resizes with 1 pixel to avoid mainUI bugs in mojave
        """
        a = self.root.winfo_geometry().split('+')[0]
        b = a.split('x')
        w = int(b[0])
        h = int(b[1])
        self.root.geometry('%dx%d' % (w+1, h+1))

    def changeselection(self):
        """
        what happens when changing selection in the treeview..
        """

        itemname = self.l1.focus()
        previeweditem = self.l1.focus()
        try:
            parentname = [i["parent"]
                          for i in self.itemlist if i["name"] == itemname][0]
            index = [i for i, j in enumerate(itemlist) if j["name"] == itemname][0]
        except:
            parentname = itemlist[0]["name"]
            index = 0
        if len(parentname) > 1:
            self.tx1.config(text="previewing: {} ( parent: {} )".format(
                itemname, parentname))
        else:
            self.tx1.config(text="previewing: {}".format(itemname))

        self.e1.delete("1.0", END)
        self.e1.insert(END, self.itemlist[index]["content"])

    def edititem(self):
        """
        copies text from e1 to e2
        """
        self.e2.delete("1.0", END)
        self.e2.insert(END, e1.get("1.0", END))

        self.editeditem = self.previeweditem
        name = self.editeditem
        self.parentname = [i["parent"] for i in self.itemlist if i["name"] == name][0]
        index = [i for i, j in enumerate(self.itemlist) if j["name"] == name][0]
        if len(parentname) > 1:
            tx2.config(text="Editing: {} ( parent: {} )".format(
                name, parentname))
        else:
            tx2.config(text="Editing: {}".format(name))

    def saveitem(self):
        """
        saves text from gui back into main dictionary
        and redraws tree, and selects where we were.
        1) resave Dictionary
        2) update "edit field"
        """

        newcontent = self.e2.get("1.0", END)
        for i, k in enumerate(self.itemlist):    # update Dictionary
            if k["name"] == self.editeditem:
                self.itemlist[i]["content"] = newcontent
        if previeweditem == self.editeditem:
            self.e1.delete("1.0", END)
            self.e1.insert(END, newcontent)


mainui = UserInterface()



def createbackup(folder, filename, bkfolder):
    """
    Backups your file into a backupfolder
    """
    mytime = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        os.mkdir(bkfolder)
    except OSError:
        # folder already exists
        pass
    try:
        filefirstname = ".".join(filename.split(".")[:-1])
        targetfile = bkfolder + "/" + filefirstname + "_" + mytime + ".txt"
        copyfile(folder + "/" + filename, targetfile)
    except FileNotFoundError as e:
        print("Can't create backup!! (Error code: {} )".format(e))


previeweditem = ""
editeditem = ""


def getlengths(fpath):
    lengths = []
    with open(fpath, "rb") as f:
        chars = f.read()
        for i in chars.split(b"\r"):
            number = int(len(i)/2)
            lengths.append(number)
    return lengths










# WIP


def savefile(self):
    """
    Saves file! WIP
    """
    with open(folder + "/" + "KEYTESTout.txt", 'wb') as f:
        for item in itemlist:
            f.write(bytes(item["name"], "utf-8"))
            f.write(b"\t")
            f.write(bytes(item["content"], "utf-8"))
            f.write(b"\t")
            f.write(bytes(item["parent"], "utf-8"))
            f.write(b"\r")


# SETUP GUI
root = Tk()



itemlist = []
createbackup(folder, filename, bkfolder)
lengths = getlengths(fpath)


def readfile(fpath):
    with open(fpath, "r", encoding="utf-16") as f:
        chars = f.read()
        count = 0
        for i, length in enumerate(lengths[:-1]):
            fromnum = count
            tonum = count+lengths[i]
            chunk = str(chars[fromnum:tonum])
            count += lengths[i]
            try:
                name = str(chunk[0:].split("\t")[0])
            except:
                name = ""
            try:
                content = str(chunk[0:].split("\t")[1])
            except:
                content = ""
            try:
                parent = chunk[1:].strip().split("\t")[2]
            except:
                parent = ""
            itemlist.append(
                {"name": name, "content": content, "parent": parent})
    return itemlist


itemlist = readfile(fpath)
templist = itemlist[:]  # local copy
uniquenames = set()

while len(templist) > 0:
    for i, item in enumerate(templist):
        parent = item["parent"]
        if parent == "":
            l1.insert('', 'end', item["name"], text=item["name"])
            del templist[i]
            uniquenames.add(item["name"])
        elif parent in uniquenames:  # it exists, so lets add to it.
            l1.insert(item["parent"], 'end', item["name"], text=item["name"])
            del templist[i]
            uniquenames.add(item["name"])


def resizeui(self):
    #print("newsize")
    pass


#root.columnconfigure(1, weight=1)
# root.rowconfigure(1, weight=1)
for i in "Up,Down,Enter,Left".split(","):
    root.bind("<"+i+">", changeselection)

root.bind("<Configure>", resizeui)
width = 1200
height = 800
root.winfo_width()
root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry("{}x{}+{}+{}".format(width, height, x, y))
root.update()
root.after(0, fixUI)
root.mainloop()
