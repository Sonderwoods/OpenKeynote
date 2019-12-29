#!/usr/bin/env python
# encoding: utf-8

# OpenKeynote
# Copyright Mathias Sønderskov Nielsen 2019-2020

from shutil import copyfile
from datetime import datetime
#import db_backend as db

# from tkinter import *
# from tkinter import ttk
# from tkinter import filedialog
from pathlib import Path
import os
# import sys
# print(sys.getdefaultencoding())


class FileHandler():
    """
    Class to handle file loading and saving
    """

    def __init__(self, path=None, prebackup=True):

        self.path = path
        self.itemlist = []

        self._folder = ""
        self._dict = {}
        self._prebackup = prebackup
        self._status_standard = "Copyright Mathias Soenderskov Schaltz 2019-2020"
        self.statustext = self._status_standard
        self._statustimer = 0
        self._statuslist = []

        self.set_paths_and_backup()

    def set_paths_and_backup(self):
        if self.path != None:
            print(self.path)
            self._folder = self.path.parent
            self._filename = self.path.name
            self._bkfolder = self._folder / "BACKUP_OpenKeynote"

        if self._prebackup == True and self.path != None:
            try:
                self.status = f"Trying to backup to {self._bkfolder}"
                """
                Backups your file into a backupfolder
                """
                mytime = datetime.now().strftime("%Y%m%d_%H%M%S")
                try:
                    os.mkdir(self._bkfolder)
                except OSError:
                    pass  # folder already exists
                try:
                    targetfile = self._bkfolder / \
                        (self.path.stem + "_" + mytime + ".txt")
                    copyfile(self.path, targetfile)
                    print(f"successfully backuped {targetfile}")
                except FileNotFoundError as e:
                    print(f"Error: Can't create backup!! ( {e} )")
            except AttributeError:
                print("AttributeError on backup")

    def read_file(self, path="", skip_refresh=False):
        templist = []
        try:
            with open(path, "r", encoding="utf-16", newline="") as f:
                chars = f.read()
        except UnicodeError:
            self.set_status("Imported file failed in utf-16,"
                            " attempting iso-8859-1", override=True)
            # with open(path, "r", encoding="mac roman", newline="") as f:
            #    chars = f.read()
            with open(path, "r", encoding="iso-8859-1", newline="") as f:
                chars = f.read()

        chars = chars.split("\r")

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
            if name.startswith("#"):
                continue
            templist.append(
                {"name": name, "content": content, "parent": parent})
        nameslist = [i['name'] for i in templist]
        m, templist = (list(t)
                       for t in zip(*sorted(zip(nameslist, templist))))

        self.itemlist = templist
        if skip_refresh == False:
            self.set_status(message=f"Successfully read {path}")
        self.set_paths_and_backup()
        self.path = path
        return True

    def write_file(self, path=""):
        """
        Saves file! WIP
        """
        if path == "":
            return
        #path = path / ".test"
        try:
            with open(path, 'w', newline='') as f:
                nameslist = [i['name'].lower() for i in self.itemlist]
                m, self.itemlist = (list(t)
                                    for t in zip(*sorted(zip(nameslist, self.itemlist))))
                for i, item in enumerate(self.itemlist):
                    if len(item["name"]) > 0:
                        f.write(item["name"] + "\t")
                    f.write(item["content"])
                    if len(item["parent"]) > 0:
                        f.write("\t" + item["parent"])
                    if i < len(self.itemlist)-1:
                        f.write("\r\n")
            self.set_status(f"Successfully saved to {path}")
        except:
            self.set_status("Error trying to save the file")

    def clear_memory(self):
        """
        Closes current file
        """
        # TODO: Ask to save current file.
        self.path = ""
        self.itemlist = []

    def add_item(self, name, parent, content):
        print(f"adding {name}, {parent}, {content}")
        self.itemlist.append(
            {"name": name, "content": content, "parent": parent})
        self.set_status(message=f"succesfully added: {name.strip()}")

    def delete_item(self, item=None):
        for i, entry in enumerate(self.itemlist):
            if item == entry["name"]:
                self.itemlist.remove(entry)

    def set_status(self, message="", override=False):
        print(message)
        if len(self._statuslist) > 0 and override == False:
            self._statuslist.append(message)
        else:
            self._statuslist.append(message)
            self.statustext = message
        self._statustimer = 0

    def refresh_status(self):
        if self._statustimer < 25:
            if len(self._statuslist) > 0:
                self._statustimer += 2  # shorter delay if queued stuff
            else:
                self._statustimer += 1
        else:
            if len(self._statuslist) > 0:
                self.statustext = self._statuslist.pop(0)
            else:
                self.statustext = self._status_standard
            self._statustimer = 0
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

    def find_primary_case(self, *args):
        """
        checks database if uppercase or lowercase.
        returns:
            0: Mixed
            1: primarily UPPERCASE
            2: primarily lowercase
            3: Uppercase Start
        """
        uc = 0
        lc = 0
        uw = 0
        wc = 0
        for i in self.itemlist:
            for content in i['content']:
                for word in content.split(" "):
                    if len(word) > 0:
                        if word[0].isupper():
                            uw += 1
                            wc += 1
                        elif word[0].islower():
                            wc += 1
                        for char in word:
                            if(char.islower()):
                                lc += 1
                            elif(char.isupper()):
                                uc += 1
        if uc > lc * 10:
            return 1
        if lc > uc*8:
            if uw > wc*0.7:
                return 3
            else:
                return 2
        return 0


if __name__ == '__main__':
    from main import main
    main()
