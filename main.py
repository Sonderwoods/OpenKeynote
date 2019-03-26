from shutil import copyfile
from time import strftime
from datetime import datetime
import os
from tkinter import *
from tkinter import ttk

## Folder setups
folder = r"C:/Users/MANI/py"
filename = "MYKEYNOTEFILE.TXT"
fpath = folder + "/" + filename
bkfolder = "/KNOTE_backups/"



def fixUI():
    """
    Resizes with 1 pixel to avoid mainUI bugs in mojave
    """
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))

    ##

def createbackup():
    mytime = datetime.now().strftime("%Y%m%d_%H%M%S")
    try:
        os.mkdir(bkfolder)
    except OSError:
        pass
    copyfile(fpath, folder + bkfolder + filename + "_" + mytime)

lengths = []
rawdata = []
with open(fpath, "rb") as f:
    chars = f.read()
    for i in chars.split(b"\r"):
        number = int(len(i)/2)
        lengths.append(number)
        rawdata.append(number)
        rawdata.append(i)

def changeselection(self):
    """
    what happens when changing selection in the treeview..
    """
    e1.config(state=NORMAL)
    itemname = l1.focus()
    parentname = [i["parent"] for i in itemlist if i["name"] == itemname][0]
    index = [i for i,j in enumerate(itemlist) if j["name"] == itemname][0]
    if len(parentname)>1:
        tx1.config(text="editing: {} ( parent: {} )".format(itemname, parentname))
    else:
        tx1.config(text="editing: {}".format(itemname))
    # #tx1.config(text="editing: " + items[index].split("\t")[0])
    e1.delete("1.0", END)
    e1.insert(END, itemlist[index]["content"])
    e1.config(state=DISABLED)
    # e2.delete("1.0", END)
    # e2.insert(END, str(itemsbytes[index]))
    #
    # root.update()

def edititem(self):
    """
    copies text from e1 to e2
    """
    e2.delete("1.0", END)
    e2.insert(END, e1.get("1.0", END))

def saveitem(self):
    """
    saves text from gui back into main dictionary
    and redraws tree, and selects where we were.
    """
    pass
###SETUP GUI
root = Tk()



sf1 = Text(root, height = 1, width = 17)
sf1.grid(row = 0, column = 0)
sb1 = Button(root, text="X", width = 3)
sb1.grid(row = 0, column = 1)
sb2 = Button(root, text="X", width = 3)
sb2.grid(row = 0, column = 2)
#


#Setup treebar and scroll
l1 = ttk.Treeview(root, height=10)
yscroll = Scrollbar(root, orient=VERTICAL)
yscroll.config(width=20)
l1['yscrollcommand'] = yscroll.set
yscroll['command'] = l1.yview
l1.grid(row=1, column=0, rowspan=9, columnspan=3, sticky=N+S+E)
yscroll.grid(row=1, column=0,rowspan=9, columnspan=3, sticky=N+S+E)
l1.bind("<ButtonRelease-1>", changeselection)



#Vertical bar
vb0 = Button(root, text="0")
vb0.grid(row = 0, column = 3)
vb1 = Button(root, text="1")
vb1.grid(row = 1, column = 3)
vb2 = Button(root, text="2")
vb2.grid(row = 2, column = 3)
vb3 = Button(root, text="3")
vb3.grid(row = 3, column = 3)
vb4 = Button(root, text="4")
vb4.grid(row = 4, column = 3)
vb5 = Button(root, text="5")
vb5.grid(row = 5, column = 3)
vb6 = Button(root, text="6")
vb6.grid(row = 6, column = 3)
vb7 = Button(root, text="7")
vb7.grid(row = 7, column = 3)
vb8 = Button(root, text="8")
vb8.grid(row = 8, column = 3)
vb9 = Button(root, text="9")
vb9.grid(row = 9, column = 3)

#label
tx1 = Label(root, text="Editing", width = 50)
tx1.grid(row = 0, column = 4, columnspan=3)

#e1 = Entry(root, textvariable=entryString, width=75)
e1 = Text(root, height=14, width = 84)
e1.config(state=NORMAL, padx=10, pady=10)
e1.grid(row = 1, column = 4, columnspan=3, rowspan=4)

e2 = Text(root, height=14, width = 84)
e2.config(state=NORMAL)
e2.grid(row = 6, column = 4, columnspan=3, rowspan=4)



vb1 = Button(root, text="Edit", width = 40)
vb1.grid(row=5,column=4)
vb1.bind("<ButtonRelease-1>", edititem)
vb2 = Button(root, text="Save", width= 40)
vb2.grid(row=5,column=5)





itemlist = []
createbackup()


with open(fpath, "r", encoding="utf-16") as f:
    chunks = []
    chars = f.read()
    count = 0
    for i,length in enumerate(lengths[:-1]):
        fromnum = count
        tonum = count+lengths[i]
        chunk = str(chars[fromnum:tonum])
        count += lengths[i]
        try:
            name = str(chunk[0:].split("\t")[0])
            #print(name)
        except:
            name = ""
        try:
            content = str(chunk[0:].split("\t")[1])
            # for text in content.split("\n"):
            #     print(" -  {}".format(text))
        except:
            content = ""
        try:
            parent = chunk[1:].strip().split("\t")[2]
        except:
            parent = ""
        #print(" - ( parent: {} )".format(parent))
        #print(" ")
        itemlist.append({"name" : name, "content" : content, "parent" : parent})
        chunks.append(chunk)

templist = itemlist[:]



uniquenames = set()
while len(templist)>0:
    for i, item in enumerate(templist):
        parent = item["parent"]
        if parent == "":
            l1.insert('', 'end', item["name"], text = item["name"])
            del templist[i]
            uniquenames.add(item["name"])
        elif parent in uniquenames: #it exists, so lets add to it.
            l1.insert(item["parent"], 'end', item["name"], text = item["name"])
            del templist[i]
            uniquenames.add(item["name"])

#root.geometry("1000x400+120+120")
root.update()
root.after(0, fixUI)
root.mainloop()
