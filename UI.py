import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from UIfunctions import UIfunctions

class UserInterface(UIfunctions):
    def __init__(self, filehandler, path=None):

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
        self.sb1.bind("<ButtonRelease-1>", self.save_file_dialog)
        self.sb2 = Button(self.frame_left, text="OPENFILE", width=3)
        self.sb2.grid(row=0, column=2)
        self.sb2.bind("<ButtonRelease-1>", self.open_file_dialog)

        # Setup treebar and scroll
        self.l1 = ttk.Treeview(self.frame_left, show="tree")
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
        middlebuttons = ("New*", "New Sub*", "Delete*",
                         "Rename*", "Change Parent*")
        middlefunctions = (self.add_item, self.add_subitem, self.delete_item,
            self.rename_item, self.change_parent)
        for a, button_text in enumerate(middlebuttons):
            self.vbs.append(Button(self.frame_center, text=button_text))
            self.vbs[a].pack(fill=BOTH)
            self.vbs[a].bind("ButtonRelease-1", middlefunctions[a])
            #TODO: Binds not working BUG .
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

        menu = Menu(self.root)
        self.root.config(menu=menu)
        file = Menu(menu)
        file.add_command(label='Open File...', command=self.open_file_dialog)
        file.add_command(label='Save File', command=self.save_file)
        file.add_command(label='Save File As...', command=self.save_file_dialog)
        file.add_command(label='Close file', command=self.close_file)
        file.add_command(label='Exit', command=self.client_exit)
        menu.add_cascade(label='File', menu=file)

        menu_help = Menu(menu)
        menu_help.add_command(label='About', command=self.about)
        menu.add_cascade(label='Help', menu=menu_help)


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
        if os.name == "nt":
            self.root.bind("<Control-s>", self.save_file)
        else:
            self.root.bind("<Command-s>", self.save_file)

        if path:
            self.open_file(path=path)

        self.root.title("OpenKeynote (BETA) by Mathias Sønderskov")

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

    def client_exit(self):
        exit()

    def about(self):
        print("OpenKeynote by Mathias Sønderskov")

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

    def resizeui(self):
        # print("newsize")
        pass

if __name__ == '__main__':
    from main import main
    main()
