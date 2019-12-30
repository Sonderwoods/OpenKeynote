#!/usr/bin/env python
# encoding: utf-8

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019

import sys
from pathlib import Path
from UIfunctions import UIfunctions
import os
# from tkinter import *
from tkinter import (ttk, Tk, PanedWindow, filedialog, scrolledtext, messagebox,
                     BOTH, W, S, E, N, StringVar, IntVar, Button, Frame, Label,
                     Text, Scrollbar, LabelFrame, DISABLED, Checkbutton,
                     NORMAL, Menu, Radiobutton, HORIZONTAL, VERTICAL, END)


class UserInterface(UIfunctions):
    def __init__(self, filehandler, databasehandler, path=None):
        self.title = "OpenKeynote (BETA)"
        self._filehandler = filehandler
        self._databasehandler = databasehandler
        self.path = path
        self.itemlist = []
        self.root = Tk()
        self.previeweditem = ""
        self.editeditem = ""
        self.case_selected = IntVar()
        self.parentname = ""
        self.autosave = IntVar()

        self._default_title = self.title
        self.main_window()
        self.tree_view()
        self.frame_vertical_bar()
        self.bindings_and_menu()
        self.frame_setup()

        self.update_status()
        self.root.mainloop()

    def main_window(self, *args):
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=E+W+N+S)
        self.bottomframe = Frame(self.root)
        self.bottomframe.grid(column=0, row=1, sticky=E+W)
        self.statusbar = Label(
            self.bottomframe, text=self._filehandler.statustext, anchor=W)
        self.statusbar.pack(fill=BOTH, padx=0, pady=0)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, pad=10)
        self.pw = PanedWindow(self.mainframe, orient=HORIZONTAL)
        self.pw.pack(fill=BOTH, expand=1)
        self.pane_left = Frame(self.root)
        self.pw.add(self.pane_left)
        self.pane_right = Frame(self.root)
        self.pw.add(self.pane_right)

        self.frame_left = Frame(self.pane_left)
        self.frame_left.pack(fill=BOTH, expand=1, padx=3, pady=3)
        self.frame_center = Frame(self.pane_right)
        self.frame_center.grid(row=0, column=0, sticky=W+N, rowspan=4)
        self.frame_right = Frame(self.pane_right)
        self.frame_right.grid(row=0, column=1, sticky=W+E+N+S, padx=3, pady=3)
        self.pane_right.columnconfigure(1, weight=1)
        self.pane_right.rowconfigure(0, weight=1)
        self.sf1 = Text(self.frame_left, height=1, width=25, borderwidth=1,
                        relief="solid", highlightthickness=0)
        self.sf1.insert(1.0, "TODO: Searchbar")
        self.sf1.grid(row=0, column=0, sticky=W+E+N+S, pady=5)
        self.sf1.config(state=DISABLED)
        self.cs = Button(self.frame_left, text="X", width=1)
        self.cs.grid(row=0, column=1)
        self.frame_left.columnconfigure(0, weight=1)

    def tree_view(self, *args):
        """
        Tree view
        """
        self.l1 = ttk.Treeview(self.frame_left, columns=["stuff"], show="tree")
        self.yscroll = Scrollbar(self.frame_left, orient=VERTICAL)
        self.yscroll.config(width=10)
        self.l1['yscrollcommand'] = self.yscroll.set
        self.yscroll['command'] = self.l1.yview
        self.l1.grid(row=1, column=0, columnspan=3,  padx=30,
                     pady=10, sticky=N+S+E+W)
        self.yscroll.grid(row=1, column=0, columnspan=3, sticky=N+S+E)
        self.l1.bind("<ButtonRelease-1>", self.change_selection)

        self.frame_left.rowconfigure(1, weight=1)

    def frame_vertical_bar(self, *args):
        self.vbs = []
        middlebuttons = ("New Item", "New Subitem", "Delete",
                         "Rename", "Change Parent","- Descriptions (BETA) -")
        middlefunctions = (
            lambda: self.add_item(parent=self.parentname),
            lambda: self.add_item(parent=self.previeweditem),
            lambda: self.delete_item_dialog(),
            self.rename_item_dialog,
            self.change_parent_dialog,
            lambda: self.description_window(database_rows=self._databasehandler.view())
            #lambda: self.save_keynote_to_database(title="title",keynote="KN10", entreprise="min entreprise", category="")
            #self.save_all_keynotes_to_database
            )

        for a, button_text in enumerate(middlebuttons):
            self.vbs.append(ttk.Button(self.frame_center, text=button_text))
            self.vbs[a].pack(fill=BOTH)
            self.vbs[a].config(command=middlefunctions[a], width=10)
        for x in [2, 3, 4]:
            self.vbs[x].config(state=DISABLED)
        self.tx1 = Label(self.frame_right, text="Preview", anchor=W)
        self.tx1.grid(row=0, column=0, columnspan=3, sticky=W+E)
        self.tx2 = Label(self.frame_right, text="Editing", anchor=W)
        self.tx2.grid(row=2, column=0, sticky=W+E)

        self.e1 = scrolledtext.ScrolledText(self.frame_right,
                                            fg="#555", font=("Courier", 13),
                                            padx=10, pady=10,
                                            highlightthickness=0,
                                            borderwidth=1, relief="solid")
        self.e1.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W)
        # was Text before

        self.e2 = scrolledtext.ScrolledText(self.frame_right,
                                            font=("Courier", 13), borderwidth=1,
                                            relief="solid", padx=10, pady=10,
                                            highlightthickness=0)
        self.e2.grid(row=3, column=0, columnspan=3, sticky=E+W+S+N)
        # AUTOSAVE
        self.autosaveFrame = LabelFrame(self.frame_center, text=' Autosave ')
        self.autosaveFrame.pack(fill=BOTH)
        self.autosave.trace(
            'w', lambda *args: print(f"Autosave: {self.autosave.get()}"))
        self.autosaveCheck = Checkbutton(
            self.autosaveFrame, text="Enabled", variable=self.autosave, anchor=W)
        self.autosaveCheck.select()
        self.autosaveCheck.pack(fill=BOTH)
        self.labelsFrame = LabelFrame(self.frame_center, text=' Change Case ')
        self.labelsFrame.pack(fill=BOTH)

        # CASE BUTTONS
        self.case_radiobuttons = []
        self.case_selected.set(99)
        rbtns = ['No change', 'UPPERCASE', 'lowercase', 'First Letter']
        for a, button_text in enumerate(rbtns):
            self.case_radiobuttons.append(
                Radiobutton(self.labelsFrame, text=button_text,
                            variable=self.case_selected,
                            value=a, command=self.change_case, width=10, anchor=W))
            self.case_radiobuttons[a].grid(sticky="W", row=a)

    def change_case(self, *args):
        pass

    def bindings_and_menu(self, *args):
        """
        Main key bindings
        """
        if os.name == "nt":
            self.CTRL = "Control"
            self.MBTN = "3"
        else:
            self.CTRL = "Command"
            self.MBTN = "2"

        def bindings_key(event):
            if event.state == 8 or event.state == 12:
                return
            else:
                return("break")

        self.sf1.bind("<Tab>", lambda a: self.focus_on(target=self.l1))
        self.sf1.bind("<Shift-Tab>", lambda a: self.focus_on(target=self.vb2))
        self.e1.bind("<Key>", bindings_key)
        self.e1.bind("<Tab>", lambda a: self.focus_on(target=self.e2))
        self.e1.bind(
            "<Shift-Tab>", lambda a: self.focus_on(target=self.vbs[-1]))

        self.e2.bind("<Tab>", lambda a: self.focus_on(target=self.vb1))
        self.e2.bind("<Shift-Tab>", lambda a: self.focus_on(target=self.e1))

        self.vb1 = ttk.Button(self.frame_right, text="Edit")
        self.vb1.grid(row=2, column=1)
        self.vb1.config(command=self.edit_item)
        self.vb2 = ttk.Button(self.frame_right, text="Save")
        self.vb2.grid(row=2, column=2)
        self.vb2.config(command=self.saveitem)

        self.frame_right.rowconfigure(1, weight=1)
        self.frame_right.rowconfigure(3, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        file = Menu(self.menu, tearoff=0)  # TODO is it a win thing?
        file.add_command(label='New File*', command=self.close_file)
        file.add_command(
            label='Open File...', accelerator=f"{self.CTRL}-o",
            command=self.open_file_dialog)
        file.add_command(label='Save File',
                         accelerator=f"{self.CTRL}-s", command=self.save_file)
        file.add_command(label='Save File As...',
                         command=self.save_file_dialog)
        file.add_command(label='Close file', command=self.close_file)
        file.add_command(
            label='Exit', accelerator=f"{self.CTRL}-q", command=self.client_exit)
        self.menu.add_cascade(label='File', menu=file)

        self.clickmenu = Menu(self.root, tearoff=0)
        self.clickmenu.add_command(label="Cut")
        self.clickmenu.add_command(label="Copy")
        self.clickmenu.add_command(label="Paste")
        self.root.bind_class(
            "Text", f"<Button-{self.MBTN}><ButtonRelease-{self.MBTN}>",
            lambda event=None: self.right_click_menu())

        menu_edit = Menu(self.menu, tearoff=0)
        menu_edit.add_command(label='Select All', accelerator=f"{self.CTRL}-a",
                              command=self.select_all)
        self.root.bind(f"<{self.CTRL}-a>", self.select_all)
        self.e1.bind(f"<{self.CTRL}-a>", self.select_all)

        self.e1.bind(f"<{self.CTRL}-c>", self.e1.event_generate("<<Copy>>"))
        self.e2.bind(f"<{self.CTRL}-a>", self.select_all)
        menu_edit.add_command(label='Cut', accelerator=f"{self.CTRL}-x",
                              command=lambda: self.root.event_generate("<<Cut>>"))
        menu_edit.add_command(label='Copy', accelerator=f"{self.CTRL}-c",
                              command=lambda: self.copy_text())
        menu_edit.add_command(label='Paste', accelerator=f"{self.CTRL}-v",
                              command=lambda: self.root.event_generate("<<Paste>>"))
        self.menu.add_cascade(label='Edit', menu=menu_edit)

        menu_help = Menu(self.menu, tearoff=0)
        menu_help.add_command(label='About', command=self.about)
        self.menu.add_cascade(label='Help', menu=menu_help)

        for i in "Up,Down,Right,Return,Left".split(","):
            self.root.bind("<"+i+">", self.change_selection)

        self.e1.bind("<F2>", self.rename_item_dialog)
        self.e1.bind(f"<{self.CTRL}-s>", None)
        self.e1.bind(f"<{self.CTRL}-o>", None)
        self.root.bind("<F2>", self.rename_item_dialog)
        self.root.bind(f"<{self.CTRL}-s>", self.save_file)
        self.root.bind(f"<{self.CTRL}-o>", self.open_file_dialog)

    def copy_text(self, event=None):
        w = self.root.focus_get()
        w.event_generate("<<Copy>>")

    def update_title(self, title=""):
        self.root.title(title)

    def frame_setup(self, *args):
        """
        Misc UI functions
        """

        # sharp fonts in high res (https://stackoverflow.com/questions/41315873/
        # attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
        if os.name == "nt":
            # TODO
            # self.root.protocol("WM_DELETE_WINDOW", self.client_exit)
            from ctypes import windll, pointer, wintypes
            try:
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass  # this will fail on Windows Server and maybe early Windows
            # TODO: Put link to ico file on windows.
            try:
                iconpath = Path("icon.ico")
                self.root.iconbitmap(Path())
            except:
                print("error with icon")
            else:  # mac?
                self.root.createcommand('exit', self.client_exit)

        self.root.title(self.title)
        if self.path:
            self.open_file(path=self.path)

        """ TODO: ICON /Windows

        self.root.iconbitmap("/Users/msn/Dropbox/py/Git/OpenKeynote/images/ico.icns")

        img = Image(
            "photo", file="/Users/msn/Dropbox/py/Git/OpenKeynote/images/large.gif")
        self.root.iconphoto(True, img) # you may also want to try this.
        self.root.call('wm','iconphoto', self.root._w, img)
        """
        self.width = min(int(self.root.winfo_screenwidth()-500), 1500)
        self.height = int(self.root.winfo_screenheight()-500)
        self.root.winfo_width()
        self.root.winfo_height()
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        # self.x = 0
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        # self.y = 50
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.root.update()
        self.root.after(0, self.fixUI)

    def right_click_menu(self, event=None):
        x, y = self.root.winfo_pointerxy()
        w = self.root.winfo_containing(x, y)
        # https://stackoverflow.com/a/8476726/11514850
        # w = self.root
        self.clickmenu.entryconfigure("Cut",
                                      command=lambda: w.event_generate("<<Cut>>"))
        self.clickmenu.entryconfigure("Copy",
                                      command=lambda: w.event_generate("<<Copy>>"))
        self.clickmenu.entryconfigure("Paste",
                                      command=lambda: w.event_generate("<<Paste>>"))
        self.clickmenu.tk.call("tk_popup", self.clickmenu,
                               w.winfo_pointerx(), w.winfo_pointery())

    def update_status(self, event=None):
        """
        Set statusbar in bottom of the window
        """
        self.statusbar.config(text=self._filehandler.refresh_status())
        self.root.after(100, self.update_status)

    def client_exit(self, *args):
        answer = messagebox.askyesnocancel('quit?', 'Save file first?')
        if answer == True:
            self.save_file()
            sys.exit()
        if answer == None:
            return
        if answer == False:
            exit()


if __name__ == '__main__':
    from main import main
    main()
