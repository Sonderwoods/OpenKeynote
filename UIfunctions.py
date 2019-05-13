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

    def new_file(self, button=""):
        self._filehandler.setstatus("Missing New file function")

    def add_item(self, button=""):
        self._filehandler.setstatus("TODO: Add button")

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
