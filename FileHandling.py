from shutil import copyfile
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import io
import os
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019


class FileHandler():
    """
    Class to handle file loading and saving
    """

    def __init__(self, path=None, prebackup=True):
        self._dict = {}
        self.path = path
        self.itemlist = []

        self._prebackup = prebackup

        self.path = self.path.replace("\\", "/")

        if self.path == None:
            self.open_file()
        else:
            self.open_file(path=path)

        self._folder = "/".join(self.path.split("/")[:-1])
        self._filename = self.path.split("/")[-1]
        self._bkfolder = self._folder + "/KNOTE_backups"

        if self._prebackup == True:
            print(f"Trying to backup to {self._bkfolder}")
            self.createbackup(self._folder, self._filename, self._bkfolder)

        #self.open_file()

    def open_file(self, button=None, path=None):
        # if self.path != None:
        #    self.close_file()
        if path == None:
            self.path = filedialog.askopenfilename(
                initialdir="/",
                title="Open File",
                filetypes=(("text files", "*.txt"), ("All files", "*.*")))
            if self.path == "":
                print("Canceled file open")
                return False
            print(f"Opening {self.path}")

            # Encoding stuff : https://www.devdungeon.com/content/working-binary-data-python
            self.itemlist = []
        else:
            self.path = path

        with open(self.path, "r", encoding="utf-16", newline="") as f:
            chars = f.read().split("\r")

            for chunk in chars:
                try:
                    name = str(chunk[0:].split("\t")[0]).strip()
                except IndexError:
                    name = ""
                try:
                    content = str(chunk[0:].split("\t")[1])
                except IndexError:
                    content = ""
                try:
                    parent = chunk[1:].strip().split("\t")[2].strip()
                except IndexError:
                    parent = ""
                self.itemlist.append(
                    {"name": name, "content": content, "parent": parent})
            self.itemlist = sorted(self.itemlist, key=lambda i: i['name'] in self.itemlist)
        return True

    def close_file(self):
        """
        Closes current file
        """
        # TODO: Ask to save current file.
        self.path = ""
        self.itemlist = []


    def createbackup(self, folder, filename, bkfolder):
        """
        Backups your file into a backupfolder
        """
        mytime = datetime.now().strftime("%Y%m%d_%H%M%S")
        try:
            os.mkdir(bkfolder)
        except OSError:
            pass  # folder already exists
        try:
            filefirstname = ".".join(filename.split(".")[:-1])
            targetfile = bkfolder + "/" + filefirstname + "_" + mytime + ".txt"
            copyfile(folder + "/" + filename, targetfile)
        except FileNotFoundError as e:
            print(f"Error: Can't create backup!! ( {e} )")

    def save_file(self, button):
        """
        Saves file! WIP
        """
        # TODO self.path ...
        filepath = self._folder + "/" + "KEYTESTout.txt"
        try:
            with open(filepath, 'w', newline='') as f:
                for i, item in enumerate(self.itemlist):
                    if len(item["name"]) > 0:
                        f.write(item["name"] + "\t")
                    f.write(item["content"])
                    if len(item["parent"]) > 0:
                        f.write("\t" + item["parent"])
                    if i < len(self.itemlist)-1:
                        f.write("\r\n")
            print(f"Successfully saved to {filepath}")
        except:
            print("Error trying to save the file")
