from shutil import copyfile
from datetime import datetime
import os
from tkinter import *
from tkinter import ttk
import sys

# sharp fonts in high res (https://stackoverflow.com/questions/41315873/
# attempting-to-resolve-blurred-tkinter-text-scaling-on-windows-10-high-dpi-disp)
if os.name == "nt":
    from ctypes import windll, pointer, wintypes
    try:
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass  # this will fail on Windows Server and maybe early Windows


# filepaths
fpath = "/Users/msn/Dropbox/py/Git/OpenKeynote/MYKEYNOTEFILE.TXT"
fpath = r"C:\Users\MANI\py\MYKEYNOTEFILE.TXT"
fpath = fpath.replace("\\", "/")
folder = "/".join(fpath.split("/")[:-1])

filename = fpath.split("/")[-1]
bkfolder = folder + "/KNOTE_backups"

# overrules premade filepath with cmd prompt input.
args = sys.argv
if len(sys.argv) > 1:
    fpath = sys.argv[-1]


def fixUI():
    """
    Resizes with 1 pixel to avoid mainUI bugs in mojave
    """
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1, h+1))


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


def changeselection(self):
    """
    what happens when changing selection in the treeview..
    """
    global previeweditem

    itemname = l1.focus()
    previeweditem = l1.focus()
    parentname = [i["parent"] for i in itemlist if i["name"] == itemname][0]
    index = [i for i, j in enumerate(itemlist) if j["name"] == itemname][0]
    if len(parentname) > 1:
        tx1.config(text="previewing: {} ( parent: {} )".format(
            itemname, parentname))
    else:
        tx1.config(text="previewing: {}".format(itemname))

    e1.delete("1.0", END)
    e1.insert(END, itemlist[index]["content"])


def edititem(self):
    """
    copies text from e1 to e2
    """
    e2.delete("1.0", END)
    e2.insert(END, e1.get("1.0", END))

    global previeweditem
    global editeditem

    editeditem = previeweditem
    itemname = editeditem
    parentname = [i["parent"] for i in itemlist if i["name"] == itemname][0]
    index = [i for i, j in enumerate(itemlist) if j["name"] == itemname][0]
    if len(parentname) > 1:
        tx2.config(text="Editing: {} ( parent: {} )".format(
            itemname, parentname))
    else:
        tx2.config(text="Editing: {}".format(itemname))


def saveitem(self):
    """
    saves text from gui back into main dictionary
    and redraws tree, and selects where we were.
    1) resave Dictionary
    2) update "edit field"
    """
    global itemlist
    global editeditem
    global previeweditem

    newcontent = e2.get("1.0", END)
    for i, k in enumerate(itemlist):    # update Dictionary
        if k["name"] == editeditem:
            itemlist[i]["content"] = newcontent
    if previeweditem == editeditem:
        e1.delete("1.0", END)
        e1.insert(END, newcontent)

# WIP


def savefile(self):
    """
    Saves file! WIP

    with open(folder + "/" + "KEYTESTout.txt", mode="wb") as f:
        for s in [1,2,3]:
            x = str(s)
            # print(x, file=f)
            string = "test\n"
            b = bytes(string, 'utf-8')
            print(b, file=f)
            print(b"\r".decode("utf-8"), file=f)
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

pw = PanedWindow(root, orient=HORIZONTAL)

pw.pack(fill=BOTH, expand=1)

pane_left = Frame(root)
pw.add(pane_left)
#pane_left.grid(row=0, column=0, sticky=E+W+N+S)
#pane_left.rowconfigure(1, weight=1)
#pane_left.columnconfigure(1, weight=1)


pane_right = Frame(root)
#pane_right.grid(row=0, column=2, sticky=E+W+N+S)
pw.add(pane_right)

frame_left = Frame(pane_left)
frame_left.pack(fill=BOTH, expand=1)
frame_center = Frame(pane_right)
frame_center.grid(row=0, column=0, sticky=E+W+N+S)
frame_right = Frame(pane_right)
frame_right.grid(row=0, column=1, sticky=E+W+N+S)

sf1 = Text(frame_left, height=1, width=17)
sf1.grid(row=0, column=0)
sb1 = Button(frame_left, text="SAVEFILE", width=15)
sb1.grid(row=0, column=1)
sb1.bind("<ButtonRelease-1>", savefile)
sb2 = Button(frame_left, text="X", width=3)
sb2.grid(row=0, column=2)

# Setup treebar and scroll
l1 = ttk.Treeview(frame_left)
yscroll = Scrollbar(frame_left, orient=VERTICAL)
yscroll.config(width=20)
l1['yscrollcommand'] = yscroll.set
yscroll['command'] = l1.yview
l1.grid(row=1, column=0, columnspan=3,  padx=(
    30), pady=(10), sticky=N+S+E+W)
yscroll.grid(row=1, column=0, columnspan=3, sticky=N+S+E)
l1.bind("<ButtonRelease-1>", changeselection)

frame_left.rowconfigure(1, weight=1)
frame_left.columnconfigure(0, weight=1)

vbs = []  # Vertical bar
for a in range(10):
    vbs.append(Button(frame_center, text=str(a)))
    vbs[a].pack(fill=BOTH)
    # vbs[a].grid(row=int(a)+1)

# label
tx1 = Label(frame_right, text="Preview", width=50)
tx1.grid(row=0, column=0, columnspan=3)
tx2 = Label(frame_right, text="Editing", width=50)
tx2.grid(row=2, column=0)

e1 = Text(frame_right, fg="#555", font=("Courier", 15),
          padx=10, pady=10)
e1.grid(row=1, column=0, columnspan=3)

e2 = Text(frame_right, font=("Courier", 15), borderwidth=3,
          relief="solid", padx=10, pady=10)
e2.grid(row=3, column=0, columnspan=3)

vb1 = Button(frame_right, text="Edit", width=20)
vb1.grid(row=2, column=1)
vb1.bind("<ButtonRelease-1>", edititem)
vb2 = Button(frame_right, text="Save", width=20)
vb2.grid(row=2, column=2)
vb2.bind("<ButtonRelease-1>", saveitem)

frame_right.rowconfigure(0, weight=1)
frame_right.rowconfigure(1, weight=1)

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
    print("newsize")
    print(frame_left.winfo_width())


root.columnconfigure(2, weight=1)
#root.rowconfigure(1, weight=1)


root.bind("<Configure>", resizeui)
width = 1000
height = 500
root.winfo_width()
root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry("{}x{}+{}+{}".format(width, height, x, y))
root.update()
root.after(0, fixUI)
root.mainloop()
