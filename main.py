from shutil import copyfile
from datetime import datetime
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sys

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019

class UserInterface():

    def __init__(self, filehandler):
        self._filehandler = filehandler
        self.itemlist = []
        self.root = Tk()
        self.previeweditem = ""
        self.editeditem = ""


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
        self.sb1.bind("<ButtonRelease-1>", self._filehandler.savefile)
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

        # sharp fonts in high res (https://stackoverflow.com/questions/41315873/
        # attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
        if os.name == "nt":
            from ctypes import windll, pointer, wintypes
            try:
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass  # this will fail on Windows Server and maybe early Windows



        #root.columnconfigure(1, weight=1)
        # root.rowconfigure(1, weight=1)
        for i in "Up,Down,Enter,Left".split(","):
            self.root.bind("<"+i+">", self.changeselection)

        #self.root.bind("<Configure>", self.resizeui)
        self.width = 1200
        self.height = 800
        #self.root.winfo_width()
        #self.root.winfo_height()
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        #self.root.update()
        #self.root.after(0, self.fixUI)
        self.root.mainloop()

    def fixUI(self):
        if os.name != "nt":
            """
            Resizes with 1 pixel to avoid mainUI bugs in mojave
            """
            a = self.root.winfo_geometry().split('+')[0]
            b = a.split('x')
            w = int(b[0])
            h = int(b[1])
            self.root.geometry('%dx%d' % (w+1, h+1))

    def changeselection(self, button):
        """
        what happens when changing selection in the treeview..
        """
        itemlist = self._filehandler.itemlist
        itemname = self.l1.focus()
        #print(itemlist)
        #print(itemname)

        self.previeweditem = self.l1.focus()
        try:
            parentname = [i["parent"] for i in itemlist if i["name"] == itemname][0]
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
        self.e1.insert(END, itemlist[index]["content"])

    def edititem(self, button):
        """
        copies text from e1 to e2
        """
        itemlist = self._filehandler.itemlist
        self.e2.delete("1.0", END)
        self.e2.insert(END, self.e1.get("1.0", END))

        self.editeditem = self.previeweditem
        name = self.editeditem
        self.parentname = [i["parent"] for i in itemlist if i["name"] == name]
        index = [i for i, j in enumerate(itemlist) if j["name"] == name]
        #TODO eventualt [0] after name] above 2 lines.
        if len(self.parentname) > 1:
            self.tx2.config(text="Editing: {} ( parent: {} )".format(
                name, parentname))
        else:
            self.tx2.config(text="Editing: {}".format(name))

    def saveitem(self, button):
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
        if self.previeweditem == self.editeditem:
            self.e1.delete("1.0", END)
            self.e1.insert(END, newcontent)

    def updateTree(self):
        itemlist = self._filehandler.itemlist #gets from FileHandler
        uniquenames = set()
        while len(itemlist) > 0:
            for i, item in enumerate(itemlist):
                parent = item["parent"]
                if parent == "":
                    self.l1.insert('', 'end', item["name"], text=item["name"])
                    del itemlist[i]
                    uniquenames.add(item["name"])
                elif parent in uniquenames:  # it exists, so lets add to it.
                    self.l1.insert(item["parent"], 'end', item["name"], text=item["name"])
                    del itemlist[i]
                    uniquenames.add(item["name"])
    def resizeui(self):
        #print("newsize")
        pass



class FileHandler():
    """
    Class to handle file loading and saving
    """


    def __init__(self, path = None, prebackup = True):
        self._dict = {}
        self.path = path
        self.itemlist = []

        self._prebackup = prebackup
        if self.path == None:
            self.open_file()
        self.path = self.path.replace("\\", "/")

        self._folder = "/".join(self.path.split("/")[:-1])
        self._filename = self.path.split("/")[-1]
        self._bkfolder = self._folder + "/KNOTE_backups"

        if self._prebackup == True:
            print(f"Trying to backup to {self._bkfolder}")
            self.createbackup(self._folder, self._filename, self._bkfolder)


        self.open_file()
        # filepaths

        # overrules premade filepath with cmd prompt input.

    def open_file(self):
        if self.path != None:
            self.close_file()
        self.path = filedialog.askopenfilename(
            initialdir = "/",
            title = "Open File",
            filetypes = (("text files", "*.txt"), ("All files", "*.*")))
        print(f"Opening {self.path}")

        self._lengths = []
        with open(self.path, "rb") as f:
            chars = f.read()
            for i in chars.split(b"\r"):
                number = int(len(i)/2)
                self._lengths.append(number)
        # Encoding stuff : https://www.devdungeon.com/content/working-binary-data-python


        self.itemlist = []
        with open(self.path, "r", encoding="utf-16") as f:
            chars = f.read()
            count = 0
            for i, length in enumerate(self._lengths[:-1]):
                fromnum = count
                tonum = count+self._lengths[i]
                chunk = str(chars[fromnum:tonum])
                count += self._lengths[i]
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
                self.itemlist.append(
                    {"name": name, "content": content, "parent": parent})


    def close_file(self):
        """
        Closes current file
        """
        pass
        #Ask to save current file.
        #Close current file.

    def createbackup(self, folder, filename, bkfolder):
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
            print(f"Can't create backup!! (Error code: {e} )")


    def savefile(self, button):
        """
        Saves file! WIP
        """
        #TODO self.path ...
        with open(self._folder + "/" + "KEYTESTout.txt", 'wb') as f:
            for item in self.itemlist:
                f.write(bytes(item["name"], "utf-8"))
                f.write(b"\t")
                f.write(bytes(item["content"], "utf-8"))
                f.write(b"\t")
                f.write(bytes(item["parent"], "utf-8"))
                f.write(b"\r")


def main(path = None):
    """
    main loop
    """
    if len(sys.argv) > 1:
        path = sys.argv[-1]
    if path != None:
        filehandler = FileHandler(path)
    else:
        filehandler = FileHandler()
    mainui = UserInterface(filehandler = filehandler)

if os.name == "nt":
    path = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
else:
    path = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"

if __name__ == '__main__':
    main(path)
