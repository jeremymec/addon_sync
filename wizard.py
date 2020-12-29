from tkinter import *
from tkinter.filedialog import askdirectory
import json

class SetupWizard:

    def __init__(self):
        self.master = Tk()
        self.master.minsize(400, 150)
        self.master.title("Addon Sync Setup")
        self.location_screen()
        self.master.mainloop()

    def selectCallBack(self):
        self.result = askdirectory()
        self.directory_textbox.delete(0, END)
        self.directory_textbox.insert(END, self.result)

    def nextCallBack(self):

        config_data = {}
        config_data['WowFolder'] = self.result

        with open('config.json', 'w+') as f:

            f.write()
    
    def location_screen(self):
        location_label = Label(self.master, text="Please select the location of your World of Warcraft installation.")
        location_label.grid(row=0, columnspan=2, pady=10)

        directory_button = Button(self.master, text="Select Folder", command = self.selectCallBack)
        directory_button.grid(row=1, column=0, sticky=E, padx=5)

        self.directory_textbox = Entry(self.master, width=48)
        self.directory_textbox.grid(row=1, column=1, sticky=W, pady=30)

        next_button = Button(self.master, text="Next", command = self.nextCallBack)
        next_button.grid(row=2, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    main = SetupWizard()


