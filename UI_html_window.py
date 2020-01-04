import tkinter as tk
from tkinter import (ttk, Tk, filedialog, messagebox,
                     BOTH, W, S, E, N, StringVar, IntVar, Button, Frame, Label,
                     Text, Scrollbar, LabelFrame, Entry, DISABLED,
                     NORMAL, Menu, HORIZONTAL, VERTICAL, END, LEFT, Y, X, NO, YES)
from tkinter.font import Font
from multicolumn_Listbox import Multicolumn_Listbox
from markdown import markdown

#from cefpython_openkeynote import MainFrame
#from tkinterhtml import HtmlFrame
#from cefpython3 import cefpython as cef
import tk_html_widgets
from tk_html_widgets import HTMLLabel

class HTMLPreview():
    def __init__(self, html, column="", col=0,rowID=0):

        def update_html(input="", btn=None):
            self.html_text = markdown(input)
            self.dw_htmllabel.set_html(self.html_text)
            self.dw_htmllabel.fit_height()

        rnframe = Tk()

        rnframe.title(f"OpenKeyote - Editing {column}")
        rnframe.geometry(f"900x500+{1000}+{500}")
        rnname = Text(rnframe, font=("Courier", 8),
                            padx=10, pady=10, highlightthickness=1,
                            borderwidth=1, relief="solid", height=10)
        rnname.grid(row=1, column=0, sticky=E+W, padx=10, pady=10)
        rnname.delete("1.0", END)
        rnname.insert(END, html)
        rnname.focus()
        rnname.mark_set('insert', '1.0')

        htmlframe = Frame(rnframe, height=500)
        htmlframe.grid(row=2, column=0)
        self.dw_htmllabel = HTMLLabel(htmlframe, html=markdown("#hi\nnice"))
        #self.dw_htmllabel.grid(row=2, column=0)
        self.dw_htmllabel.pack(fill="both", expand=True)
        #self.dw_htmllabel.fit_height()

        rnframe.columnconfigure(1, weight=1)
        rnframe.rowconfigure(1, weight=1)
        rnokbtn = ttk.Button(rnframe, text="OK", width=10)
        rnokbtn.grid(row=4, column=0, sticky=N+W, padx=5, pady=10)
        rnokbtn.config(command=lambda: self.dw_submit(titles=self._dw_t1_rows,
            col = self._dw_t1_column, data=rnname.get("1.0", "end-1c"), frame=rnframe))
        rncancelbtn = ttk.Button(rnframe, text="Cancel",
                                 command=rnframe.destroy)
        rncancelbtn.grid(row=4, column=1, sticky=N+W+E, padx=5, pady=10)
        rnname.bind("<KeyRelease>", lambda e=None: update_html(rnname.get("1.0", "end-1c")))
        rnframe.mainloop()

if __name__ == '__main__':
    htmlframe = HTMLPreview("#header\n##subheader\ntext...")
    #from main import main
    #main()
