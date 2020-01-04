#!/usr/bin/env python
# encoding: utf-8

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019

import os
import tkinter as tk
from tkinter import (ttk, Tk, filedialog, messagebox,
                     BOTH, W, S, E, N, StringVar, IntVar, Button, Frame, Label,
                     Text, Scrollbar, LabelFrame, Entry, DISABLED,
                     NORMAL, Menu, HORIZONTAL, VERTICAL, END, LEFT, Y, X, NO, YES)
from tkinter.font import Font
from pathlib import Path
from multicolumn_Listbox import Multicolumn_Listbox
from markdown import markdown
import pdfkit
import tempfile
#from cefpython_openkeynote import MainFrame
#from tkinterhtml import HtmlFrame
#from cefpython3 import cefpython as cef
import tk_html_widgets
from tk_html_widgets import HTMLLabel
#from UI_html_window import HTMLPreview





class UIfunctions():
    """
    Handles all the UI functions. called by UI.py
    """
    def __str__(self):
        text = ["First five lines:"]
        try:
            for i in self.itemlist[0:5]:
                text.append(f"name: {i['name']}, \tcontent: {i['content']}, \
                    \tparent: {i['parent']}")
            return "\n".join(text)
        except:
            return "empty"

    def open_file_dialog(self, event=None):
        path = filedialog.askopenfilename(
            initialdir=self._filehandler._folder,
            title="Open File",
            filetypes=(("text files", "*.txt"), ("All files", "*.*")))
        if path == "" or path == None:
            self._filehandler.set_status("Cancelled file open")
            return False
        else:
            self.open_file(path=Path(path))

    def open_file(self, path, skip_refresh=False):

        self._filehandler.itemlist = []
        self.itemlist = []
        self._filehandler.path = path
        self.e1.delete("1.0", END)
        if skip_refresh == False:
            self.e2.delete("1.0", END)
            self._filehandler.set_status(f"Opening {path}")
        self._filehandler.read_file(path=path, skip_refresh=skip_refresh)
        print(f"path = {path.parent} ... fname = {path.stem}")
        dbpath = path.parent.joinpath(f"{path.stem}.db")
        self._databasehandler.connect(path=dbpath, current_itemlist=self._filehandler.itemlist)
        self.update_tree(skip_refresh=True)
        self.change_selection(skip_refresh=True)
        self.update_title(self._default_title + " - " + str(path))
        self.check_case()

    def save_file_dialog(self, event=None):
        path = filedialog.asksaveasfilename(
            initialdir=self._filehandler._folder,
            title="Save File",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        if path != None and path != "":
            self._filehandler.path = Path(path)
            self.save_file(path=self._filehandler.path)

    def save_file(self, e=None, path=""):
        if path == "":
            if self._filehandler.path != "" and self._filehandler.path != None:
                path = self._filehandler.path
            else:
                self._filehandler.set_status(
                    "Warning: tried to save unknown path")
                return False
        self._filehandler.write_file(path)
        self.update_title(self._default_title + " - " + str())

    def close_file(self):
        self.e1.delete("1.0", END)
        self.e2.delete("1.0", END)
        self._filehandler.clear_memory()
        self.l1.delete(*self.l1.get_children())
        self.update_tree()
        self.change_selection()
        self.update_title(title=self._default_title)
        self._filehandler.path = ""

    def add_item(self, event=None, parent=""):
        def validate_input(name="", parent="", btn=None):
            if name in self._filehandler.get_names() or len(name) == 0:
                btn.config(state=DISABLED)
                return False
            if parent not in self._filehandler.get_names() and len(parent) > 0:
                btn.config(state=DISABLED)
                return False
            btn.config(state=NORMAL)
            return True
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        absx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        absy = self.root.winfo_pointery() - self.root.winfo_rooty()
        self.newframe = Tk()
        self.newframe.title("Add an item")
        self.newframe.geometry(f"400x400+{x+50}+{y-20}")
        catlabel = Label(self.newframe, text="Parent (category):")
        catlabel.grid(row=1, column=0)
        namelabel = Label(self.newframe, text="Name:")
        namelabel.grid(row=2, column=0)
        contentlabel = Label(self.newframe, text="Content")
        contentlabel.grid(row=3, column=0)
        self.cattext = Text(self.newframe, font=("Courier", 13),
                            padx=10, pady=10, highlightthickness=1,
                            borderwidth=1, relief="solid", height=1)
        self.cattext.grid(row=1, column=1, sticky=E+W)
        self.nametext = Text(self.newframe, font=("Courier", 13),
                             padx=10, pady=10, highlightthickness=1,
                             borderwidth=1, relief="solid", height=1)
        self.nametext.grid(row=2, column=1, sticky=E+W)
        self.contenttext = Text(self.newframe, font=("Courier", 13),
                                padx=10, pady=10, highlightthickness=1,
                                borderwidth=1, relief="solid")
        self.contenttext.grid(row=3, column=1, sticky=N+S+E+W)
        self.newframe.columnconfigure(1, weight=1)
        self.newframe.rowconfigure(3, weight=1)
        self.okbtn = ttk.Button(self.newframe, text="OK", width=10)
        self.okbtn.grid(row=4, column=0, sticky=N+W, padx=5, pady=10)
        self.okbtn.config(command=self.submit_item)
        self.cattext.insert(END, parent)
        self.cancelbtn = ttk.Button(self.newframe, text="Cancel",
                                    command=self.newframe.destroy)
        self.cancelbtn.grid(row=4, column=1, sticky=N+W+E, padx=5, pady=10)
        self.newframe.bind("<Escape>", lambda a: self.newframe.destroy())
        self.nametext.focus()
        # Tried this using lists without luck.
        self.nametext.bind("<KeyRelease>", lambda a: validate_input(
            name=self.nametext.get("1.0", "end-1c"),
            parent=self.cattext.get("1.0", "end-1c"),
            btn=self.okbtn))
        self.nametext.bind(
            "<Tab>", lambda a: self.focus_on(target=self.contenttext))
        self.nametext.bind(
            "<Return>", self.submit_item)
        self.nametext.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.cattext))
        self.cattext.bind("<KeyRelease>", lambda e=None: validate_input(
            name=self.nametext.get("1.0", "end-1c"),
            parent=self.cattext.get("1.0", "end-1c"),
            btn=self.okbtn))
        self.cattext.bind(
            "<Tab>", lambda a: self.focus_on(target=self.nametext))
        self.cattext.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.cancelbtn))
        self.contenttext.bind(
            "<Tab>", lambda a: self.focus_on(target=self.okbtn))
        self.contenttext.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.nametext))
        self.okbtn.bind("<Tab>", lambda a: self.focus_on(
            target=self.cancelbtn))
        self.okbtn.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.contenttext))
        self.cancelbtn.bind(
            "<Tab>", lambda a: self.focus_on(target=self.cattext))
        self.cancelbtn.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.okbtn))
        self.newframe.focus_force()

    def submit_item(self, event=None):
        self.auto_load()
        name = self.nametext.get("1.0", "end-1c").strip()
        parent = self.cattext.get("1.0", "end-1c").strip()
        content = self.contenttext.get(
            "1.0", "end-1c").replace("\n\r", "\n").strip()
        self._filehandler.add_item(name, parent, content)
        self.auto_save()
        self.update_tree(selection=name, parent=parent)
        self.newframe.destroy()

    def edit_item(self, event=None):
        """
        copies text from e1 to e2
        """
        self.auto_load()
        print("autosave=1")
        itemlist = self._filehandler.itemlist
        self.e2.delete("1.0", END)
        self.e2.insert(END, self.e1.get("1.0", "end-1c"))
        self.e2.focus()
        self.e2.mark_set('insert', '1.0')

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
        self.auto_save() # BUG DOES IT WORK?

    def auto_load(self):
        if self.autosave.get() == 1:
            self.refresh_file

    def auto_save(self):
        if self.autosave.get() == 1:
            self.save_file(path=self._filehandler.path)

    def saveitem(self, event=None):
        """
        saves text from gui back into main dictionary
        and redraws tree, and selects where we were.
        1) resave Dictionary
        2) update "edit field"

                0: Mixed
                1: primarily UPPERCASE
                2: primarily lowercase
                3: Uppercase Start
        """
        newcontent = self.e2.get("1.0", "end-1c")
        print(f"saving.. case is {self.case_selected.get()}")
        if self.case_selected.get() == 1:
            newcontent = str(newcontent).upper()
        if self.case_selected.get() == 2:
            newcontent = str(newcontent).lower()
        if self.case_selected.get() == 3:
            newcontent = str(newcontent).title()
        self.auto_load()
        for i, k in enumerate(self.itemlist):    # update Dictionary
            if k["name"] == self.editeditem:
                self._filehandler.itemlist[i]["content"] = newcontent
        if self.previeweditem == self.editeditem:
            self.e1.delete("1.0", END)
            #self.e1.insert(END, str(newcontent).upper())
            self.e1.insert(END, str(newcontent))
        self.auto_save()

    def delete_item_dialog(self, event=None):
        def delete_it(*args):
            self.delete_items(items=items, frame=rnframe)
        items = self.l1.selection()
        if len(items) > 1:
            item = ", ".join(items)[0:20]
        else:
            item = items[0]
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        absx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        absy = self.root.winfo_pointery() - self.root.winfo_rooty()
        rnframe = Tk()
        rnframe.title(f"Delete {item}")
        rnframe.geometry(f"500x100+{x+50}+{y-20}")
        namelabel = Label(rnframe, text=f"Deleting {item}. Are you sure?")
        namelabel.grid(row=2, column=0, padx=10, pady=10)
        rnframe.columnconfigure(1, weight=1)
        rnframe.rowconfigure(1, weight=1)
        rncancelbtn = ttk.Button(rnframe, text="No",
                                 command=rnframe.destroy, underline=0, width=8)
        rncancelbtn.grid(row=4, column=1, sticky=N+W, padx=3, pady=10)
        rnokbtn = ttk.Button(rnframe, text="Yes",
                             width=8, underline=0)
        rnokbtn.grid(row=4, column=0, sticky=N+W, padx=3, pady=10)
        rnokbtn.config(command=delete_it)
        rnframe.bind("<Escape>", lambda e=None: rnframe.destroy())
        rnokbtn.focus()
        rnframe.bind("<y>", delete_it)
        rnframe.bind("<n>", lambda e=None: rnframe.destroy())
        rnokbtn.bind("<Return>", delete_it)
        rncancelbtn.bind("<Return>", lambda e=None: rnframe.destroy)
        for i in ["Tab", "Right"]:
            rnokbtn.bind(f"<{i}>", delete_it)
        for i in ["Shift-Tab", "Left"]:
            rncancelbtn.bind(
                f"<{i}>", lambda e=None: self.focus_on(target=rnokbtn))
        rnframe.focus_force()

    def delete_items(self, event=None, items=[], frame=None):
        self.auto_load()
        for item in items:
            print(f"trying to delete {item}")
            if item in self._filehandler.get_names():
                mytree = self.get_all_children(self.l1, item)
                for i in mytree:
                    self._filehandler.delete_item(i)
                self._filehandler.delete_item(item)
        self.update_tree(selection=self._filehandler.get_parent(item))
        if len(items) > 1:
            self._filehandler.set_status(f"Deleted {len(items)} items")
        else:
            self._filehandler.set_status(f"Deleted {item}")
        if frame:
            frame.destroy()
        self.auto_save()

    def rename_item_dialog(self, event=None):
        if len(self.l1.selection()) == 0:
            return

        def validate_input(input="", btn=None):
            if input in self._filehandler.get_names() or len(input) == 0:
                rnokbtn.config(state=DISABLED)
                return False
            else:
                rnokbtn.config(state=NORMAL)
                return True
        item = self.previeweditem
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        absx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        absy = self.root.winfo_pointery() - self.root.winfo_rooty()
        rnframe = Tk()
        rnframe.title(f"OpenKeyote - Renaming {item}")
        rnframe.geometry(f"400x100+{x+50}+{y-20}")
        namelabel = Label(rnframe, text=f"Renaming {item} to:")
        namelabel.grid(row=2, column=0, padx=10, pady=10)
        rnname = Entry(rnframe, font=("Courier", 13),
                       highlightthickness=1,
                       borderwidth=1, relief="solid")
        rnname.grid(row=2, column=1, sticky=E+W, padx=10, pady=10)
        rnframe.columnconfigure(1, weight=1)
        rnframe.rowconfigure(1, weight=1)
        rnokbtn = ttk.Button(rnframe, text="OK", width=10, state=DISABLED)
        rnokbtn.grid(row=4, column=0, sticky=N+W, padx=5, pady=10)
        rnokbtn.config(command=lambda: self.rename_item(
            frame=rnframe, oldname=item, newname=rnname.get()))
        rncancelbtn = ttk.Button(rnframe, text="Cancel",
                                 command=rnframe.destroy)
        rncancelbtn.grid(row=4, column=1, sticky=N+W+E, padx=5, pady=10)
        rnframe.bind("<Escape>", lambda e=None: rnframe.destroy())
        rnframe.bind("<Return>", lambda e=None: self.rename_item(
            frame=rnframe, oldname=item, newname=rnname.get()))
        rnname.focus()
        # Tried this using lists without luck.
        rnname.bind("<KeyRelease>", lambda a: validate_input(
            input=rnname.get(), btn=rnokbtn))
        rnname.bind("<Tab>", lambda a: self.focus_on(target=rnokbtn))
        rnname.bind("<Shift-Tab>", lambda a: self.focus_on(target=rncancelbtn))
        rnokbtn.bind("<Tab>", lambda a: self.focus_on(target=rncancelbtn))
        rnokbtn.bind("<Shift-Tab>", lambda a: self.focus_on(target=rnname))
        rncancelbtn.bind("<Tab>", lambda a: self.focus_on(target=rnname))
        rncancelbtn.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=rnokbtn))
        rnframe.focus_force()

    def rename_item(self, event=None, frame=None, oldname="", newname=""):
        if len(newname) == 0:
            return
        frame.destroy()
        self.auto_load()
        self._filehandler.rename_item(oldname=oldname, newname=newname)
        self._databasehandler.rename_item(oldname=oldname, newname=newname)
        self.auto_save()
        self.update_tree(selection=newname)

    def save_keynote_to_database(self, keynote="", title="", entreprise="", category=""):
        db.insert(
        title = title,
        keynote = keynote,
        entreprise = entreprise,
        category = category
        )

    def save_all_keynotes_to_database(self):
        print("test")
        print(type(self._filehandler.itemlist))
        print(len(self._filehandler.itemlist))
        for entry in self._filehandler.itemlist:
            print(entry)
            """db.insert(
            title = title,
            keynote = keynote,
            entreprise = entreprise,
            category = category
            )"""

    def change_parent_dialog(self, Event=None):
        def validate_input(input="", btn=None):
            if input in self._filehandler.get_names():
                rnokbtn.config(state=NORMAL)
            else:
                rnokbtn.config(state=DISABLED)
        items = self.l1.selection()
        if len(items) > 1:
            item = "multiple items"
        else:
            item = items[0]
        oldparent = self.parentname
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        absx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        absy = self.root.winfo_pointery() - self.root.winfo_rooty()
        rnframe = Tk()
        rnframe.title(f"OpenKeyote - Change parent for: {item}")
        rnframe.geometry(f"400x100+{x+50}+{y-20}")
        namelabel = Label(rnframe, text=f"Change parent from {oldparent} to:")
        namelabel.grid(row=2, column=0, padx=10, pady=10)
        rnname = Entry(rnframe, font=("Courier", 13),
                       highlightthickness=1,
                       borderwidth=1, relief="solid")
        rnname.grid(row=2, column=1, sticky=E+W, padx=10, pady=10)
        rnframe.columnconfigure(1, weight=1)
        rnframe.rowconfigure(1, weight=1)
        rnokbtn = ttk.Button(rnframe, text="OK", width=10)
        if len(items) > 1:
            item = "multiple items"
            rnokbtn.config(text=f"OK (editing {len(items)} items)", width=20)
        else:
            item = self.previeweditem
        rnokbtn.grid(row=4, column=0, sticky=N+W, padx=5, pady=10)
        rnokbtn.config(command=lambda: self.change_parent_submit(
            frame=rnframe, items=items, newparent=rnname.get()))
        rncancelbtn = ttk.Button(rnframe, text="Cancel",
                                 command=rnframe.destroy)
        rncancelbtn.grid(row=4, column=1, sticky=N+W+E, padx=5, pady=10)
        rnframe.bind("<Escape>", lambda a: rnframe.destroy())
        rnname.focus()
        rnname.bind("<KeyRelease>", lambda a: validate_input(
            input=rnname.get(), btn=rnokbtn))
        rnname.bind("<Tab>", lambda a: self.focus_on(target=rnokbtn))
        rnname.bind("<Shift-Tab>", lambda a: self.focus_on(target=rncancelbtn))
        rnname.bind("<Return>", lambda a: self.change_parent_submit(
            frame=rnframe,
            items=items,
            newparent=rnname.get()
        ))

        rnokbtn.bind("<Tab>", lambda a: self.focus_on(target=rncancelbtn))
        rnokbtn.bind("<Shift-Tab>", lambda a: self.focus_on(target=rnname))
        rncancelbtn.bind("<Tab>", lambda a: self.focus_on(target=rnname))
        rncancelbtn.bind("<Shift-Tab>", lambda a: self.focus_on(target=rnokbtn))
        rnframe.focus_force()

    def change_parent_submit(self, event=None, frame=None, items=[], newparent=""):
        self.auto_load()
        if newparent == "":
            for item in items:
                self._filehandler.change_parent(
                    item=item, newparent=newparent)
        else:
            if newparent not in self._filehandler.get_names():
                return
        for item in items:
            if item != newparent:
                self._filehandler.change_parent(
                    item=item, newparent=newparent)
        self.auto_save()
        self.update_tree(selection=items[0])
        frame.destroy()

    def get_on_off_dict(self):
        previous_tree = self.get_all_children(self.l1)
        on_off_dict = {}
        for item in previous_tree:
            name = self.l1.item(item)['text']
            open = self.l1.item(item)['open']
            if open == 1:
                open = True
            else:
                open = False
            on_off_dict[name] = open
        return on_off_dict

    def refresh_file(self):
        """
        Reopens file but keeps selection etc.
        """
        on_off_dict = self.get_on_off_dict()
        item = self.previeweditem
        self.open_file(self._filehandler.path, skip_refresh=True)
        self.update_tree(selection=item)
        for itemname in on_off_dict.keys():
            if self.l1.item(itemname)['open'] == 1:
                self.l1.item(itemname, open=1)

    ##
    ## TEXT FORMATTING
    ##



    def resfresh_dw(self, event=None):
        return

    def categories_window(self, event=None, category=None):
        print("todo: Categories window")
        return

    def dw_selectItem(self, event):
        """
        what happens when click an item in the table
        """
        curItem = self.dw_t1.interior.item(self.dw_t1.interior.focus())
        curItems = self.dw_t1.selected_rows
        ids = []
        self._dw_t1_rows = [item[0] for item in curItems]

        for item in curItems:
            print(item[0])
            #ids.append(item['values'][0])
        ids = ",".join(ids)
        ids = "IDS: %s" % ids
        print(ids)
        #print("\n".join([str(self.dw_t1.interior.item(i)['values']) for i in curItems]))
        #print(curItem)
        title = curItem['values'][0]
        col = self.dw_t1.interior.identify_column(event.x)
        cols = Multicolumn_Listbox.List_Of_Columns(self.dw_t1)
        print(cols)
        try:
            col = int(col.replace('#',''))-1
        except:
            col = 0
        self._dw_t1_column = col
        #print ('curItem = ', curItem)


        columns = self.dw_columns
        cell_value = ""
        if col == 0:
            cell_value = title
        else:
            for i, column in enumerate(self.dw_columns):
                if col == i:
                    cell_value = curItem['values'][i][0:40]
        print (f"\nColumn {col}: '{self.dw_columns[col]}' - {title}")
        print(f"--\n{cell_value[0:20]}\n--")

        # elif col == '#1':
        #     cell_value = curItem['values'][0]
        # elif col == '#2':
        #     cell_value = curItem['values'][1]
        # elif col == '#3':
        #     cell_value = curItem['values'][2]
        # print ('cell_value = ', cell_value)

    def description_window(self, event=None, database_rows=None):

        item = self.previeweditem

        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        absx = self.root.winfo_pointerx() - self.root.winfo_rootx()
        absy = self.root.winfo_pointery() - self.root.winfo_rooty()

        self.dw = Tk() #description window

        self.dw.title(f"OpenKeyote - Descriptions overview")
        self.dw.geometry(f"1400x800+{700}+{200}")

        style = ttk.Style(self.dw)
        #font=Font(family='Arial', size=1)
        style.configure('Descriptions.Treeview', rowheight=80)
        self.dw_topframe = Frame(self.dw)
        self.dw_topframe.config(height=150)
        self.dw_topframe.grid(column=0, row=0, sticky=E+W)
        self.dw.rowconfigure(1, weight=1)
        self.dw.columnconfigure(0, weight=1)

        def on_select(data):
            # print(f"called command when row is selected {data}")
            pass

        self.dw_columns = ("Keynote", "Keynote Text", "Short Desc", "Long Desc", "Entreprise", "Category")
        self.dw_t1 = Multicolumn_Listbox(self.dw, self.dw_columns, style='Descriptions.Treeview', command=on_select, cell_anchor="nw")

        for i, col in enumerate(self.dw_columns):
            if i == 0:
                width=70
                minwidth=70
                stretch=False
            else:
                width=Font().measure(col)
                stretch=True
                minwidth=170
            self.dw_t1.interior.column(i, width=width, minwidth=minwidth, stretch=stretch)
        self.dw_t1.bind('<ButtonRelease-1>', self.dw_selectItem)
        self.dw_t1.bind('<ButtonRelease-3>', self.dw_edit_item_dialog)
        for i, row in enumerate(database_rows):
            self.dw_t1.insert_row(row[1:])

        self.dw_t1.interior.grid(column=0, row=1, sticky=E+W+N+S)
        self.dw_yscroll = Scrollbar(self.dw, orient=VERTICAL)
        self.dw_yscroll.config(width=15)
        #
        self.dw_t1.interior['yscrollcommand'] = self.dw_yscroll.set
        self.dw_yscroll['command'] = self.dw_t1.interior.yview
        # self.dw_t1.interior.grid(row=1, column=0,  padx=5,
        #             pady=5, sticky=N+S+E+W)
        self.dw_yscroll.grid(row=1, column=0, sticky=N+S+E)
        #self.dw_t1.bind("<ButtonRelease-1>", myfunctions)

        self.dw_vbs = []
        # buttons = ("Refresh", "Categories...", "Entreprises...")
        # functions = (
        #     self.resfresh_dw,
        #     lambda: self.categories_window(category="categories"),
        #     lambda: self.categories_window(category="entreprises"),
        #     )

        buttons = (
        ("Refresh",self.resfresh_dw),
        ("*Categories...",lambda: self.categories_window(category="categories")),
        ("Entreprises...",lambda: self.categories_window(category="entreprises")),
        ("*Print PDF...",lambda: self.print_pdf)
        )
        for button, function in buttons:
            self.dw_vbs.append(ttk.Button(self.dw_topframe, text=button))
            self.dw_vbs[-1].pack(side=LEFT, fill=Y)
            self.dw_vbs[-1].config(command=function, width=12)
        # for a, button_text in enumerate(buttons):
        #     self.dw_vbs.append(ttk.Button(self.dw_topframe, text=button_text))
        #     self.dw_vbs[a].pack(side=LEFT, fill=Y)
        #     self.dw_vbs[a].config(command=functions[a], width=12)

    def print_pdf(self, html_text, target):
        """
        not finished
        """
        try:
            pdf_file = open('lol2.pdf', 'w')
            pdf_file.write("")
            pdf_file.close()
            pdf_path = str(Path("lol2.pdf"))
        except:
            print("pdf file locked - is it open?")
        os.chmod(pdf_path, 0o777)
        config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        try:
            pdfkit.from_string(self.html_text, pdf_path, configuration=config)
        except OSError:
            print("Error - install wkhtmltopdf")

    def dw_edit_item_dialog(self, event=None):

        curItems = self.dw_t1.selected_rows
        col = self.dw_t1.interior.identify_column(event.x)
        try:
            col = int(col.replace('#',''))-1
        except:
            col = 0
        self._dw_t1_column = col
        self._dw_t1_rows = [item[0] for item in curItems]
        selected_column = self.dw_columns[col]
        item = "[" + ', '.join(self._dw_t1_rows) + "]"
        print("column")
        print(self._dw_t1_column)
        print("rows:")
        print(self._dw_t1_rows)

        x = self.dw.winfo_pointerx()
        y = self.dw.winfo_pointery()
        absx = self.dw.winfo_pointerx() - self.dw.winfo_rootx()
        absy = self.dw.winfo_pointery() - self.dw.winfo_rooty()
        rnframe = Tk()
        rnframe.title(f"OpenKeyote - Editing {selected_column}")
        rnframe.geometry(f"900x500+{800}+{400}")
        #namelabel = Label(rnframe, text=f"Editing {selected_column} for {item}:")
        #namelabel.grid(row=0, column=0, padx=10, pady=10)
        rnname = Text(rnframe, font=("Courier", 9),
                            padx=10, pady=10, highlightthickness=1,
                            borderwidth=1, relief="solid", height=10)
        rnname.grid(row=0, column=0, sticky=N+S+E+W, padx=10, pady=10)

        if len(self.dw_t1.selected_rows) == 1:
            print(self.dw_t1.selected_rows)
            text = self._databasehandler.search(title=self.dw_t1.selected_rows[0][0])
            rnname.delete("1.0", END)
            rnname.insert(END, text[0][col+1])
            rnname.focus()
            rnname.mark_set('insert', '1.0')
        # BUG : MARKDOWN NOT WORKING IN THE BELOW...
        def update_html(input="", btn=None):
            pass
        #     self.html_text = markdown(str(input))
        #     self.dw_htmllabel.set_html(self.html_text)
        #     self.dw_htmllabel.fit_height()
        #
        # htmlframe = Frame(rnframe, height=500)
        # htmlframe.grid(row=2, column=0)
        # self.dw_htmllabel = HTMLLabel(htmlframe, html=markdown(text[0][col+1]))
        # self.dw_htmllabel.pack(fill="both", expand=True)
        # self.dw_htmllabel.fit_height()

        rnframe.columnconfigure(0, weight=1)
        rnframe.rowconfigure(0, weight=1)
        botframe = Frame(rnframe, height=80)
        botframe.grid(row=1, column=0, sticky=N+W, padx=5, pady=10)
        rnokbtn = ttk.Button(botframe, text="OK", width=10)
        rnokbtn.pack(side=LEFT)
        rnokbtn.config(command=lambda: self.dw_submit(titles=self._dw_t1_rows,
            col = self._dw_t1_column, data=rnname.get("1.0", "end-1c"), frame=rnframe))
        rncancelbtn = ttk.Button(botframe, text="Cancel",
                                 command=rnframe.destroy)
        rncancelbtn.pack(side=LEFT)
        # rnframe.bind("<Escape>", lambda e=None: rnframe.destroy())
        #rnframe.bind("<Return>", lambda e=None: self.dw_save_item(
        #    frame=rnframe, oldname=item, newname=rnname.get()))
        # rnname.focus()
        rnname.bind("<KeyRelease>", lambda e=None: update_html(rnname.get("1.0", "end-1c")))
        # rnname.bind("<Tab>", lambda a: self.focus_on(target=rnokbtn))
        # rnname.bind("<Shift-Tab>", lambda a: self.focus_on(target=rncancelbtn))
        # rnokbtn.bind("<Tab>", lambda a: self.focus_on(target=rncancelbtn))
        # rnokbtn.bind("<Shift-Tab>", lambda a: self.focus_on(target=rnname))
        # rncancelbtn.bind("<Tab>", lambda a: self.focus_on(target=rnname))
        # rncancelbtn.bind(
        #     "<Shift-Tab>", lambda a: self.focus_on(target=rnokbtn))
        # rnframe.focus_force()
        rnframe.mainloop()

    def dw_submit(self, event=None, titles=None, col = None, data=None, frame=None):
        if len(titles) == 0:
            return
        frame.destroy()
        #self.auto_load()
        #self._filehandler.rename_item(oldname=oldname, newname=newname)
        for title in titles:
            lookup_lines = self._databasehandler.search(title=title)
            for lookup_line in lookup_lines:
                lookup_line = list(lookup_line)
                print("\nSUBMITTING\n--")
                print(lookup_line)
                print(col)
                print(f"column = {col} ... data is {lookup_line[col+1]}")
                print(f"database ID {lookup_line[0]}")
                lookup_line[col+1] = data
                self._databasehandler.update(
                    id=lookup_line[0],
                    title=lookup_line[1],
                    keynote=lookup_line[2],
                    short_description=lookup_line[3],
                    long_description=lookup_line[4],
                    entreprise=lookup_line[5],
                    category=lookup_line[6]
                )
                ## ToDO NOT DONE
                self.dw_t1.column[1] = ["item1", "item2"]

        #self._databasehandler.rename_item(oldname=oldname, newname=newname)
        #self.auto_save()
        #self.update_tree()

    def dw_rename(self, event=None, frame=None, oldname="", newname=""):
        if len(newname) == 0:
            return
        frame.destroy()
        self.auto_load()
        self._filehandler.rename_item(oldname=oldname, newname=newname)
        self._databasehandler.rename_item(oldname=oldname, newname=newname)
        self.auto_save()
        self.update_tree(selection=newname)

    def update_tree(self, selection=None, parent=None, op="", skip_refresh=False):

        if selection == None:
            selection = self.l1.focus()

        self.itemlist = self._filehandler.itemlist  # gets from FileHandler
        itemlist = self.itemlist[:]   # temp list that we can delete from
        uniquenames = set()
        on_off_dict = self.get_on_off_dict()

        self.l1.delete(*self.l1.get_children())

        nameslist = [i['name'] for i in itemlist]
        m, itemlist = (list(t)
                       for t in zip(*sorted(zip(nameslist, itemlist))))
        while len(itemlist) > 0:
            for i, item in enumerate(itemlist):
                if item["name"] not in uniquenames:
                    if item["name"] == "":
                        del itemlist[i]
                        continue
                    if item["parent"] == "":
                        try:
                            self.l1.insert(
                                '', 'end', item["name"], text=item["name"])
                            if op == "Expand":
                                self.l1.item(item["name"], open=True)
                            elif op == "Collapse":
                                self.l1.item(item["name"], open=False)
                            else:
                                if item["name"] in on_off_dict.keys():
                                    if on_off_dict[item["name"]]:
                                        self.l1.item(item["name"], open=True)
                                    else:
                                        self.l1.item(item["name"], open=False)
                        except TclError:
                            self._filehandler.set_status('Warning: Tried '
                                                         f'to add item {item["name"]},'
                                                         'but it was already in the list')
                        del itemlist[i]
                        uniquenames.add(item["name"])
                    # it exists, so lets add to it.
                    elif item["parent"] in uniquenames:
                        self.l1.insert(item["parent"], 'end',
                                       item["name"], text=item["name"])
                        del itemlist[i]
                        uniquenames.add(item["name"])
                else:
                    del itemlist[i]
        if parent != None and parent != "":
            self.l1.item(parent, open=True)

        ts = selection
        while self._filehandler.get_parent(ts):
            ap = self._filehandler.get_parent(ts)
            if ap != False:
                self.l1.item(ap, open=True)
                ts = ap

        # self.l1.selection_clear()
        if selection in self._filehandler.get_names():
            self.l1.selection_set(selection)
            self.l1.focus(selection)
        self.change_selection(skip_refresh=True)
        self.l1.heading("stuff", text="stuff",
                        command=lambda c="stuff": treeview_sort_column(self.l1, c, False))

    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
            #      ^^^^^^^^^^^^^^^^^^^^^^^
        except ValueError:
            l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        tv.heading(col, command=lambda: self.treeview_sort_column(
            tv, col, not reverse))

        # self.l1.focus_set
    def check_case(self, *args):
        primcase = self._filehandler.find_primary_case()
        self.case_selected.set(primcase)
        print(f"case selected: {str(primcase)}")

    def change_selection(self, event=None, skip_refresh=False):
        """
        what happens when changing selection in the treeview..
        """
        itemlist = self._filehandler.itemlist
        itemname = self.l1.focus()
        if len(itemlist) == 0:
            self.vbs[0].config(state=NORMAL, text="New Item")
            self.vbs[1].config(state=DISABLED, text="New Subitem")
            self.vbs[2].config(state=DISABLED, text="Delete")
            self.vbs[3].config(state=DISABLED, text="Rename")
            self.vbs[4].config(state=DISABLED, text="Change Parent")
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
        ls = self.l1.selection()
        self.vbs[2].config(state=NORMAL)
        self.vbs[3].config(state=NORMAL)
        self.vbs[4].config(state=NORMAL)
        self.vbs[2].config(text=f"Delete {self.previeweditem}")
        if len(ls) < 1:
            self.vbs[2].config(state=DISABLED)
            self.vbs[3].config(state=DISABLED)
            self.vbs[4].config(state=DISABLED)
        if len(ls) > 1:
            self.vbs[3].config(state=DISABLED)
            for i in ls:
                if self._filehandler.get_parent(item=i) != self._filehandler.get_parent(item=ls[0]):
                    self.vbs[4].config(state=DISABLED)
            self.vbs[4].config(text=f"Change Parents")
        else:
            self.vbs[4].config(text="Change Parent")
        if len(self.parentname) > 0:
            self.vbs[0].config(text=f"New Item ({self.parentname})")
            self.vbs[1].config(state=DISABLED)
        else:
            self.vbs[0].config(text=f"New Item")
        cs = self.get_all_children(self.l1, self.previeweditem)
        if len(cs) > 0 and len(self.previeweditem) > 0:
            self.vbs[2].config(
                text=f"Delete {self.previeweditem} and {len(cs)} children")
        if len(ls) > 1:
            self.vbs[2].config(text=f"Delete {len(ls)} items")
        if len(self.previeweditem) > 0 and len(ls) == 1:
            self.vbs[1].config(state=NORMAL)
            self.vbs[1].config(text=f"New Subitem ({self.previeweditem})")
        else:
            self.vbs[1].config(state=DISABLED)
            self.vbs[1].config(text=f"New Subitem")

    def select_all(self, event=None):
        self.root.focus_get().tag_add('sel', '1.0', 'end-1c')
        #self.root.focus_get().tag_add('sel', '1.0', END-1)

    def focus_next(self, event=None):
        event.tk_focusNext().focus()
        return("break")

    def focus_prev(self, event=None):
        event.tk_focusPrev().focus()
        return("break")

    def focus_on(self, event=None, target=""):
        target.focus()
        return("break")

    def about(self, event=None):
        messagebox.showinfo("About OpenKeynote",
                            "OpenKeynote\n2019, Mathias Sønderskov Nielsen\n\
For more info - www.github.com/sonderwoods")

    def treeview_sort_column(self, tv, col, reverse):
        object = self.l1
        l = [(object.set(k, col), k) for k in object.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            object.move(k, '', index)

        # reverse sort next time
        # TODO
        object.heading(col, command=lambda:
                       self.treeview_sort_column(tv, col, not reverse))

    def fixUI(self, event=None, win=None):
        """
        Resizes with 1 pixel to avoid mainUI bugs in mojave
        """
        if os.name != "nt":
            if win == None:
                win = self.root

            a = win.winfo_geometry().split('+')[0]
            b = a.split('x')
            w = int(b[0])
            h = int(b[1])
            win.geometry('{}x{}'.format(w+1, h+1))

    def get_all_children(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.get_all_children(tree, child)
        return children

    def html_wrap_in_css(selv, html):
        from inspect import getsourcefile
        from os.path import abspath
        cur_path = Path(abspath(getsourcefile(lambda:0)))
        cur_folder = cur_path.parent
        css_path = cur_folder / "assets" / "air.css"
        with open(css_path) as file:
            cssfile = file.read()
        html = "<!DOCTYPE html><html><head></head><body>\n" + html + "\n</body></html>"
        return html


if __name__ == '__main__':
    from main import main
    main()
