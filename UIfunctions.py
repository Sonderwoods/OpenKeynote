import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019


class UIfunctions():
    """
    Handles all the UI functions. called by UI.py
    """

    def open_file_dialog(self,button=""):
        path = filedialog.askopenfilename(
            initialdir=self._filehandler._folder,
            title="Open File",
            filetypes=(("text files", "*.txt"), ("All files", "*.*")))
        if path == "" or path == None:
            #print("Canceled file open")
            self._filehandler.setstatus("Cancelled file open")
            return False
        else:
            self.open_file(path = path)

    def open_file(self, path):
        self._filehandler.setstatus(f"Opening {path}")
        self._filehandler.itemlist = []
        self.itemlist = []
        self._filehandler.path = path
        self._filehandler.read_file(path = path)
        self.e1.delete("1.0", END)
        self.e2.delete("1.0", END)
        self.updateTree()

    def save_file_dialog(self, button=""):
        path = filedialog.asksaveasfilename(
            initialdir=self._filehandler._folder,
            title="Save File",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if path != None and path != "":
            self._filehandler.path = path
            self.save_file(path=path)

    def about(self):
        newframe = Tk()
        newlabel = Label(newframe, text="OpenKeynote by Mathias Sønderskov "\
        "Nielsen.\nFor more info check out www.github.com/sonderwoods")
        newlabel.pack(fill=BOTH,padx = 40, pady=15)
        newframe.title("About OpenKeynote")
        bt1 = Button(newframe, text="Ok", command=newframe.destroy)
        bt1.pack(fill=BOTH,padx = 40, pady=10)
        width = 500
        height = 120
        x = (newframe.winfo_screenwidth() // 2) - (width // 2)
        y = (newframe.winfo_screenheight() // 2) - (height // 2)
        newframe.geometry(f"{width}x{height}+{x}+{y}")

    def new_file(self, button=""):
        self._filehandler.setstatus("Missing New file function")

    def add_item(self, button="", parent=""):
        newframe = Tk()
        newframe.title("Add an item")
        namelabel = Label(newframe, text="Name:")
        namelabel.grid(row=1, column=0)
        catlabel = Label(newframe, text="Parent (category):")
        catlabel.grid(row=2, column=0)

        contentlabel = Label(newframe, text="Content")
        contentlabel.grid(row=3, column=0)
        nametext = Text(newframe, font=("Courier", 13),
                       padx=10, pady=10, highlightthickness=1,
                       borderwidth=1, relief="solid", height=1)
        nametext.grid(row=1, column=1, sticky=E+W)
        cattext = Text(newframe, font=("Courier", 13),
                       padx=10, pady=10, highlightthickness=1,
                       borderwidth=1, relief="solid", height=1)
        cattext.grid(row=2, column=1, sticky=E+W)

        contenttext = Text(newframe, font=("Courier", 13),
                       padx=10, pady=10, highlightthickness=1,
                       borderwidth=1, relief="solid")
        contenttext.grid(row=3, column=1, sticky=N+S+E+W)
        newframe.columnconfigure(1, weight=1)
        newframe.rowconfigure(3, weight=1)
        okbtn = ttk.Button(newframe, text="OK** (not working)", width=10)
        okbtn.grid(row=4, column=0, sticky=N+S+E+W)
        cattext.insert(END, parent)
        cancelbtn = ttk.Button(newframe, text="Cancel", command=newframe.destroy)
        cancelbtn.grid(row=4, column=1, sticky=N+S+E+W)
        newname = nametext.get("1.0", END)
        newparent = cattext.get("1.0", END)
        newcontext = contenttext.get("1.0", END)

        self._filehandler.add_item(newname, newparent, newcontext)



    def add_subitem(self, button=""):
        self._filehandler.setstatus("TODO: Add sub item")

    def delete_item(self, button=""):
        self._filehandler.setstatus("TODO: Delete item")

    def rename_item(self, button=""):
        self._filehandler.setstatus("TODO: Rename item")

    def change_parent(self, button=""):
        self._filehandler.setstatus("TODO: Change parent")

    def save_file(self, button="", path=""):
        if path != "":
            self._filehandler.write_file(path)
        else:
            if self._filehandler.path != "" and self._filehandler.path != None:
                self._filehandler.write_file(self._filehandler.path)
            else:
                self._filehandler.setstatus("tried to save unknown path")

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
        self.parentname = parentname

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

    def treeview_sort_column(self, tv, col, reverse):
        object = self.l1
        l = [(object.set(k, col), k) for k in object.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            object.move(k, '', index)

        # reverse sort next time
        #TODO
        object.heading(col, command=lambda: \
                   self.treeview_sort_column(tv, col, not reverse))

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
                self._filehandler.itemlist[i]["content"] = newcontent
        if self.previeweditem == self.editeditem:
            self.e1.delete("1.0", END)
            self.e1.insert(END, newcontent)

    def __str__(self):
        text = ["First five lines:"]
        for i in self.itemlist[0:5]:
            text.append(f"name: {i['name']}, \tcontent: {i['content']}, \
                \tparent: {i['parent']}")
        return "\n".join(text)

    def fixUI(self, win=None):
        """
        Resizes with 1 pixel to avoid mainUI bugs in mojave
        """
        if os.name != "nt":
            if win == None:
                win = self.root

            a = win.winfo_geometry().split('+')[0]
            print(a)
            b = a.split('x')
            w = int(b[0])
            h = int(b[1])
            win.geometry('{}x{}'.format(w+1, h+1))

    def updateTree(self):
        self.itemlist = self._filehandler.itemlist  # gets from FileHandler
        itemlist = self.itemlist[:]   # temp list that we can delete from

        uniquenames = set()
        while len(itemlist) > 0:
            for i, item in enumerate(itemlist):
                parent = item["parent"]
                if parent == "":
                    try:
                        self.l1.insert(
                            '', 'end', item["name"], text=item["name"])
                    except TclError:
                        self._filehandler.setstaus(f'Error: Tried to add item\
                         {item["name"]}, but it was already in the list')
                    del itemlist[i]
                    uniquenames.add(item["name"])
                elif parent in uniquenames:  # it exists, so lets add to it.
                    self.l1.insert(item["parent"], 'end',
                                   item["name"], text=item["name"])
                    del itemlist[i]
                    uniquenames.add(item["name"])
        print(self)

    def close_file(self):
        self.e1.delete("1.0", END)
        self.e2.delete("1.0", END)
        self._filehandler.clear_memory()
        self.l1.delete(*self.l1.get_children())

if __name__ == '__main__':
    from main import main
    main()
