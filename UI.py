import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019

class UserInterface():
    """
    Handles all the UI
    """

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
        self.sb1.bind("<ButtonRelease-1>", self._filehandler.save_file)
        self.sb2 = Button(self.frame_left, text="OPENFILE", width=3)
        self.sb2.grid(row=0, column=2)
        self.sb2.bind("<ButtonRelease-1>", self._filehandler.open_file)

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
        middlebuttons = ("Up", "Down", "<-", "New", "New Sub", "Delete",
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

        self.updateTree()

        #self.root.bind("<Configure>", self.resizeui)
        self.width = 1200
        self.height = 800
        self.root.winfo_width()
        self.root.winfo_height()
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.root.update()
        self.root.after(0, self.fixUI)
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
        if len(itemlist) == 0:
            return

        self.previeweditem = self.l1.focus()
        try:
            parentname = [i["parent"]
                          for i in itemlist if i["name"] == itemname][0]
            index = [i for i, j in enumerate(
                itemlist) if j["name"] == itemname][0]
        except IndexError:
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
        # TODO eventualt [0] after name] above 2 lines.
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

    def __str__(self):
        text = []
        for i in self.itemlist[0:5]:
            text.append(f"name: {i['name']}, \tcontent: {i['content']}, \
                \tparent: {i['parent']}")
        return "\n".join(text)

    def updateTree(self):
        self.itemlist = self._filehandler.itemlist  # gets from FileHandler
        itemlist = self.itemlist[:]  # temp list that we can delete from
        print("Updating Tree")

        uniquenames = set()
        while len(itemlist) > 0:
            for i, item in enumerate(itemlist):
                parent = item["parent"]
                if parent == "":
                    try:
                        self.l1.insert(
                            '', 'end', item["name"], text=item["name"])
                    except TclError:
                        print(f'Error: Tried to add item {item["name"]}, but it\
                        was already in the list')
                    del itemlist[i]
                    uniquenames.add(item["name"])
                elif parent in uniquenames:  # it exists, so lets add to it.
                    self.l1.insert(item["parent"], 'end',
                                   item["name"], text=item["name"])
                    del itemlist[i]
                    uniquenames.add(item["name"])

    def resizeui(self):
        # print("newsize")
        pass
