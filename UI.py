import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from UIfunctions import UIfunctions

class UserInterface(UIfunctions):
    def __init__(self, filehandler, path=None):

        self._filehandler = filehandler
        self.path = path
        self.itemlist = []
        self.root = Tk()
        self.previeweditem = ""
        self.editeditem = ""

        self.main_window()
        self.tree_view()
        self.frame_vertical_bar()
        self.frame_bindings()
        self.main_menu()
        self.frame_setup()

        self.root.after(100, self.status)


    def main_window(self, *args):
        self.mainframe = Frame(self.root)
        self.mainframe.grid(column=0, row=0, sticky=E+W+N+S)
        self.bottomframe = Frame(self.root)
        self.bottomframe.grid(column=0, row=1, sticky=E+W)
        self.statusbar = Label(self.bottomframe, text=self._filehandler.statustext, anchor=W)
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
        self.sf1.grid(row=0, column=0, sticky=W+E+N+S, pady = 5)
        self.cs = Button(self.frame_left, text="X", width=1)
        self.cs.grid(row=0, column=1)
        self.frame_left.columnconfigure(0, weight=1)


    def tree_view(self, *args):
        """
        Tree view
        """
        self.l1 = ttk.Treeview(self.frame_left, show="tree")
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
                         "Rename", "Change Parent")
        middlefunctions = (
            lambda: self.add_item(parent=self.parentname),
            lambda: self.add_item(parent=self.previeweditem),
            self.delete_item, self.rename_item_dialog, self.change_parent_dialog)
        for a, button_text in enumerate(middlebuttons):
            self.vbs.append(ttk.Button(self.frame_center, text=button_text))
            self.vbs[a].pack(fill=BOTH)
            self.vbs[a].config(command=middlefunctions[a], width=20)
        for x in [2,3,4]:
            self.vbs[x].config(state=DISABLED)
        self.tx1 = Label(self.frame_right, text="Preview", anchor=W)
        self.tx1.grid(row=0, column=0, columnspan=3, sticky=W+E)
        self.tx2 = Label(self.frame_right, text="Editing", anchor=W)
        self.tx2.grid(row=2, column=0, sticky=W+E)

        self.e1 = Text(self.frame_right, fg="#555", font=("Courier", 13),
                       padx=10, pady=10, highlightthickness=0,
                       borderwidth=1, relief="solid")

        self.e1.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W)

        self.e2 = Text(self.frame_right, font=("Courier", 13), borderwidth=1,
                       relief="solid", padx=10, pady=10, highlightthickness=0)
        self.e2.grid(row=3, column=0, columnspan=3, sticky=E+W+S+N)


    def frame_bindings(self, *args):
        """
        Main key bindings
        """
        if os.name == "nt":
            self.CTRL = "Control"
        else:
            self.CTRL = "Command"

        def bindings_key(event):
            #if len(str(event.keysym)) == 1:
            return("break")
        self.e1.bind("<Key>", bindings_key)
        self.e1.bind("<Tab>", lambda a:self.focus_on(target=self.e2))
        self.e1.bind("<Shift-Tab>", lambda a:self.focus_on(target=self.vbs[-1]))

        self.e2.bind("<Tab>", lambda a:self.focus_on(target=self.vb1))
        self.e2.bind("<Shift-Tab>", lambda a:self.focus_on(target=self.e1))


        self.vb1 = ttk.Button(self.frame_right, text="Edit")
        self.vb1.grid(row=2, column=1)
        self.vb1.config(command=self.edit_item)
        self.vb2 = ttk.Button(self.frame_right, text="Save")
        self.vb2.grid(row=2, column=2)
        self.vb2.config(command=self.saveitem)

        self.frame_right.rowconfigure(1, weight=1)
        self.frame_right.rowconfigure(3, weight=1)
        self.frame_right.columnconfigure(0, weight=1)

    def main_menu(self, *args):
        """
        Main top bar menu and right click menu
        """

        menu = Menu(self.root)
        self.root.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='New File*', accelerator=f"{self.CTRL}-n", command=self.new_file)
        file.add_command(label='Open File...', accelerator=f"{self.CTRL}-o", command=self.open_file_dialog)
        file.add_command(label='Save File', accelerator=f"{self.CTRL}-s", command=self.save_file)
        file.add_command(label='Save File As...', command=self.save_file_dialog)
        file.add_command(label='Close file', command=self.close_file)
        file.add_command(label='Exit', accelerator=f"{self.CTRL}-q", command=self.client_exit)
        menu.add_cascade(label='File', menu=file)


        self.clickmenu = Menu(self.root, tearoff=0)
        self.clickmenu.add_command(label="Cut")
        self.clickmenu.add_command(label="Copy")
        self.clickmenu.add_command(label="Paste")
        self.root.bind_class("Text", "<Button-2><ButtonRelease-2>", self.right_click_menu)



        menu_edit = Menu(menu)
        menu_edit.add_command(label='Select All', accelerator=f"{self.CTRL}-a",
            command=self.select_all)
        self.root.bind(f"<{self.CTRL}-a>", self.select_all)
        self.e1.bind(f"<{self.CTRL}-a>", self.select_all)


        self.e1.bind(f"<{self.CTRL}-c>", self.root.event_generate("<<Copy>>"))
        self.e2.bind(f"<{self.CTRL}-a>", self.select_all)
        menu_edit.add_command(label='Cut', accelerator=f"{self.CTRL}-x",
            command=lambda: self.root.event_generate("<<Cut>>"))
        menu_edit.add_command(label='Copy', accelerator=f"{self.CTRL}-c",
            command=lambda: self.root.event_generate("<<Copy>>"))
        menu_edit.add_command(label='Paste', accelerator=f"{self.CTRL}-v",
            command=lambda: self.root.event_generate("<<Paste>>"))
        menu.add_cascade(label='Edit', menu=menu_edit)

        menu_help = Menu(menu)
        menu_help.add_command(label='About', command=self.about)
        menu.add_cascade(label='Help', menu=menu_help)

    def frame_setup(self, *args):
        """
        Misc UI functions
        """

        # sharp fonts in high res (https://stackoverflow.com/questions/41315873/
        # attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
        if os.name == "nt":
            from ctypes import windll, pointer, wintypes
            try:
                windll.shcore.SetProcessDpiAwareness(1)
            except Exception:
                pass  # this will fail on Windows Server and maybe early Windows

        for i in "Up,Down,Enter,Left".split(","):
            self.root.bind("<"+i+">", self.change_selection)

        self.root.bind(f"<{self.CTRL}-s>", self.save_file)
        self.root.bind(f"<{self.CTRL}-o>", self.open_file_dialog)

        if self.path:
            self.open_file(path=self.path)
        self.root.title("OpenKeynote (BETA)")

        """ TODO: ICON /Windows

        self.root.iconbitmap("/Users/msn/Dropbox/py/Git/OpenKeynote/images/ico.icns")

        img = Image("photo", file="/Users/msn/Dropbox/py/Git/OpenKeynote/images/large.gif")
        self.root.iconphoto(True, img) # you may also want to try this.
        self.root.call('wm','iconphoto', self.root._w, img)
        """
        self.width = int(self.root.winfo_screenwidth()-500)
        self.height = int(self.root.winfo_screenheight()-500)
        self.root.winfo_width()
        self.root.winfo_height()
        self.x = (self.root.winfo_screenwidth() // 2) - (self.width // 2)
        self.x = 0
        self.y = (self.root.winfo_screenheight() // 2) - (self.height // 2)
        self.y = 50
        self.root.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.root.update()
        self.root.after(0, self.fixUI)
        self.root.mainloop()

    def right_click_menu(self, event=None):
        #https://stackoverflow.com/a/8476726/11514850
        w = e.widget
        self.clickmenu.entryconfigure("Cut",
        command=lambda: w.event_generate("<<Cut>>"))
        self.clickmenu.entryconfigure("Copy",
        command=lambda: w.event_generate("<<Copy>>"))
        self.clickmenu.entryconfigure("Paste",
        command=lambda: w.event_generate("<<Paste>>"))
        self.clickmenu.tk.call("tk_popup", self.clickmenu, e.x_root, e.y_root)

    def status(self, dummy=None):
        """
        Set statusbar in bottom of the window
        """
        text = self._filehandler.getstatus()
        self.statusbar.config(text=text)
        self.root.after(100, self.status)

    def client_exit(self):
        exit()

if __name__ == '__main__':
    from main import main
    main()
