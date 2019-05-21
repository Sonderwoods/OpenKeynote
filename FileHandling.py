from shutil import copyfile
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import io
import os
# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019


class FileHandler():
    """
    Class to handle file loading and saving
    """

    def __init__(self, path=None, prebackup=True):
        self._folder = ""
        self._dict = {}
        self.path = path
        self.itemlist = []
        self.status_standard = "Copyright Mathias Sønderskov Nielsen 2019"
        self.statustext = self.status_standard
        self.statustimer = 0

        self._prebackup = prebackup

        if self.path != None:
            self.path = self.path.replace("\\", "/")
            self._folder = "/".join(self.path.split("/")[:-1])
            self._filename = self.path.split("/")[-1]
            self._bkfolder = self._folder + "/KNOTE_backups"

        if self._prebackup == True:
            try:
                self.status = f"Trying to backup to {self._bkfolder}"
                self.create_backup(
                    self._folder, self._filename, self._bkfolder)
            except AttributeError:
                pass

        # self.open_file()

    def read_file(self, path=""):
        templist = []
        with open(path, "r", encoding="utf-16", newline="") as f:
            chars = f.read().split("\r")

            for chunk in chars:
                try:
                    name = str(chunk[0:].split("\t")[0]).strip()
                    name = name.replace("\t", "")
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
                templist.append(
                    {"name": name, "content": content, "parent": parent})
            templist = sorted(templist, key=lambda i: i['name'] in templist)
        self.itemlist = templist
        self.set_status(message="Successfully read file")
        return True

    def write_file(self, path=""):
        """
        Saves file! WIP
        """
        if path == "":
            return
        path = path + ".test"
        try:
            with open(path, 'w', newline='') as f:
                for i, item in enumerate(self.itemlist):
                    if len(item["name"]) > 0:
                        f.write(item["name"] + "\t")
                    f.write(item["content"])
                    if len(item["parent"]) > 0:
                        f.write("\t" + item["parent"])
                    if i < len(self.itemlist)-1:
                        f.write("\r\n")
            print(f"Successfully saved to {path}")
        except:
            print("Error trying to save the file")

    def clear_memory(self):
        """
        Closes current file
        """
        # TODO: Ask to save current file.
        self.path = ""
        self.itemlist = []

    def create_backup(self, folder, filename, bkfolder):
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

    def add_item(self, name, parent, content):
        print(f"adding {name}, {parent}, {content}")
        self.itemlist.append(
            {"name": name, "content": content, "parent": parent})
        self.set_status(message=f"succesfully added: {name.strip()}")

    def delete_item(self, item=None):
        for i, entry in enumerate(self.itemlist):
            if item == entry["name"]:
                self.itemlist.remove(entry)

    def set_status(self, message=""):
        print(message)
        self.statustext = message
        self.statustimer = 0

    def refresh_status(self):
        if self.statustimer < 20:
            self.statustimer += 1
        else:
            self.statustimer = 0
            self.statustext = self.status_standard
        return self.statustext

    def get_names(self, event=None):
        return [x['name'] for x in self.itemlist if len(x['name']) > 0]

    def rename_item(self, oldname=None, newname=None):
        for i, item in enumerate(self.itemlist):
            if item["name"] == oldname:
                self.itemlist[i]["name"] = newname
            if item["parent"] == oldname:
                self.itemlist[i]["parent"] = newname
        self.set_status(
            f"Renamed {oldname} to {newname}, including all children.")
        print(f"renaming {oldname} to {newname}")

    def get_parent(self, item=None):
        for i in self.itemlist:
            if i["name"] == item:
                return i["parent"]
        return False

    def change_parent(self, event=None, item="", newparent=""):
        for i, entry in enumerate(self.itemlist):
            if entry["name"].strip() == str(item).strip():
                self.set_status(f"changed parent of {item} to {newparent}")
                self.itemlist[i]["parent"] = newparent
                return True
        return False


if __name__ == '__main__':
    from main import main
    main()
