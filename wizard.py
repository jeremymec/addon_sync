import json
import os
from tkinter import (DISABLED, END, NORMAL, Button, E, Entry, Frame, Label,
                     StringVar, Tk, W, filedialog, IntVar, Checkbutton)


class SetupWizard:
    def __init__(self):
        self.config_data = {"LastAction": "NONE", "ActionTime": "NONE"}
        self.master = Tk()
        self.master.minsize(400, 165)
        self.master.maxsize(400, 165)
        self.master.title("Addon Sync Setup")
        self.master.iconbitmap("sync_icon.ico")
        self.location_screen()
        self.master.mainloop()

    def write_config_data(self):
        with open("config.json", "w+") as f:
            f.write(json.dumps(self.config_data))

        f.close()

    def select_callback(self):
        self.path_to_wow = filedialog.askdirectory()
        self.directory_textbox.delete(0, END)
        self.directory_textbox.insert(END, self.path_to_wow)

    def location_next_callback(self):
        self.config_data["WowFolder"] = self.path_to_wow
        self.active_frame.destroy()
        self.create_settings_screen()

    def create_repo_callback(self):
        self.active_frame.destroy()
        self.create_repo_screen()

    def repo_back_callback(self):
        self.active_frame.destroy()
        self.settings_screen()

    def create_repo_back_callback(self):
        self.active_frame.destroy()
        self.repo_screen()

    def settings_back_callback(self):
        self.active_frame.destroy()
        self.location_screen()

    def repo_next_callbak(self):
        self.config_data["RepoURL"] = self.repo_textbox.get()
        self.write_config_data()
        self.master.destroy()

    def settings_next_callback(self):
        self.load_settings_into_config()
        self.active_frame.destroy()
        self.repo_screen()

    def load_settings_into_config(self):
        checkbox_data = []
        if self.addons_var.get() == 1:
            checkbox_data.append("Addons")
        if self.addon_settings_var.get() == 1:
            checkbox_data.append("AddonSettings")
        if self.general_settings_var.get() == 1:
            checkbox_data.append("GeneralSettings")
        if self.interface_settings_var.get() == 1:
            checkbox_data.append("InterfaceSettings")
        if self.addons_enabled_var.get() == 1:
            checkbox_data.append("AddonsEnabled")
        if self.keybinds_var.get() == 1:
            checkbox_data.append("Keybinds")
        self.config_data["ObjectsTracked"] = checkbox_data

    def directory_callback(self, var_name, var_index, operation):
        self.path_to_wow = self.directory_textbox.get()
        if self.path_to_wow:
            self.location_next_button.config(state=NORMAL)
        else:
            self.location_next_button.config(state=DISABLED)

    def repo_callback(self, var_name, var_index, operation):
        self.path_to_repo = self.repo_textbox.get()
        if self.path_to_repo:
            self.repo_next_button.config(state=NORMAL)
        else:
            self.repo_next_button.config(state=DISABLED)

    def location_screen(self):
        self.master.minsize(400, 165)
        self.master.maxsize(400, 165)
        self.active_frame = Frame(self.master)

        self.location_label = Label(
            self.active_frame,
            text="Please select the location of your World of Warcraft installation.",
        )
        self.location_label.grid(row=0, columnspan=2, pady=10)

        self.directory_button = Button(
            self.active_frame, text="Select Folder", command=self.select_callback
        )
        self.directory_button.grid(row=1, column=0, sticky=E, padx=5)

        self.directory_string = StringVar()
        self.directory_string.trace_add("write", self.directory_callback)

        self.directory_textbox = Entry(
            self.active_frame, width=48, textvariable=self.directory_string
        )
        self.directory_textbox.grid(row=1, column=1, sticky=W, pady=30)

        self.location_next_button = Button(
            self.active_frame,
            text="Next",
            command=self.location_next_callback,
            state="disabled",
        )
        self.location_next_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.active_frame.grid()

    def repo_screen(self):
        self.master.minsize(400, 165)
        self.master.maxsize(400, 165)
        self.active_frame = Frame(self.master)

        repo_label = Label(
            self.active_frame, text="Please type in the address of your github repo."
        )
        repo_label.grid(row=0, pady=30)

        self.repo_string = StringVar()
        self.repo_string.trace_add("write", self.repo_callback)

        self.repo_textbox = Entry(
            self.active_frame, width=62, textvariable=self.repo_string
        )
        self.repo_textbox.grid(row=1, padx=10, pady=0)

        self.repo_next_button = Button(
            self.active_frame,
            text="Next",
            command=self.repo_next_callbak,
            state="disabled",
        )
        self.repo_next_button.grid(
            row=2, column=0, pady=30, sticky=W, padx=100)

        self.back_button = Button(
            self.active_frame, text="Back", command=self.repo_back_callback
        )
        self.back_button.grid(row=2, column=0, sticky=W, pady=30, padx=150)

        no_repo_button = Button(
            self.active_frame,
            text="I don't have a repo",
            command=self.create_repo_callback,
        )
        no_repo_button.grid(row=2, pady=30, column=0, sticky=E, padx=85)

        self.active_frame.grid()

    def create_repo_screen(self):
        self.master.minsize(425, 190)
        self.master.maxsize(425, 190)
        self.active_frame = Frame(self.master)

        create_repo_label = Label(
            self.active_frame,
            text="In order for this program to work you will need to set up a github repository.\nThis is free and should only take a few minutes.",
        )
        create_repo_label.grid(row=0, pady=10)

        repo_instructions_label = Label(
            self.active_frame,
            text="1. Go to github.com and create an account, or if you already have one, login.\n2. Go to github.com/new and create a new repo with any name you want.\n3. Copy and paste the repo URL into the box below.",
        )
        repo_instructions_label.grid(row=1, pady=10)

        self.repo_string = StringVar()
        self.repo_string.trace_add("write", self.repo_callback)

        self.repo_textbox = Entry(
            self.active_frame, width=65, textvariable=self.repo_string
        )
        self.repo_textbox.grid(row=2, padx=10)

        self.repo_next_button = Button(
            self.active_frame,
            text="Next",
            command=self.repo_next_callbak,
            state="disabled",
        )
        self.repo_next_button.grid(row=3, sticky=W, pady=10, padx=140)

        self.back_button = Button(
            self.active_frame, text="Back",
            command=self.create_repo_back_callback
        )
        self.back_button.grid(row=3, sticky=E, pady=10, padx=140)

        self.active_frame.grid()

    def create_settings_screen(self):
        self.master.minsize(400, 165)
        self.master.maxsize(400, 165)
        self.active_frame = Frame(self.master)

        settings_info_label = Label(
            self.active_frame,
            text="Please select the data you would like to keep in sync.",
        )
        settings_info_label.grid(
            row=0, pady=10, padx=60, columnspan=2, sticky=W)

        self.addons_var = IntVar()
        self.addons_var.set(1)
        addons_checkbox = Checkbutton(
            self.active_frame, text="Addons", variable=self.addons_var)
        addons_checkbox.grid(row=1, column=0, sticky=W, padx=20)

        self.addon_settings_var = IntVar()
        addon_settings_checkbox = Checkbutton(
            self.active_frame, text="Addon Settings", variable=self.addon_settings_var)
        addon_settings_checkbox.grid(row=2, column=0, sticky=W, padx=20)

        self.general_settings_var = IntVar()
        general_settings_checkbox = Checkbutton(
            self.active_frame, text="Game Settings", variable=self.general_settings_var)
        general_settings_checkbox.grid(row=3, column=0, sticky=W, padx=20)

        self.interface_settings_var = IntVar()
        interface_settings_checkbox = Checkbutton(
            self.active_frame, text="Interface Settings", variable=self.interface_settings_var)
        interface_settings_checkbox.grid(row=1, column=1, sticky=W)

        self.addons_enabled_var = IntVar()
        addons_enabled_checkbox = Checkbutton(
            self.active_frame, text="Addons Enabled/Disabled", variable=self.addons_enabled_var)
        addons_enabled_checkbox.grid(row=2, column=1, sticky=W)

        self.keybinds_var = IntVar()
        keybinds_checkbox = Checkbutton(
            self.active_frame, text="Keybindings", variable=self.keybinds_var)
        keybinds_checkbox.grid(row=3, column=1, sticky=W)

        self.settings_next_button = Button(
            self.active_frame,
            text="Next",
            command=self.settings_next_callback,
        )
        self.settings_next_button.grid(
            row=4, columnspan=2, pady=15, padx=210, sticky=W)

        self.back_button = Button(
            self.active_frame,
            text="Back",
            command=self.settings_back_callback,
        )
        self.back_button.grid(row=4, columnspan=2, pady=15, padx=140, sticky=W)

        self.active_frame.grid()


if __name__ == "__main__":
    SetupWizard()
