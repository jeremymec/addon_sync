from tkinter import filedialog, Tk, END, Label, StringVar, Button, Entry, W, E
import json

class SetupWizard:

    def __init__(self):
        self.master = Tk()
        self.master.minsize(400, 150)
        self.master.title("Addon Sync Setup")
        self.location_screen()
        self.master.mainloop()

    def select_callback(self):
        self.result = filedialog.askdirectory()
        self.directory_textbox.delete(0, END)
        self.directory_textbox.insert(END, self.result)

    def next_callback(self):

        config_data = {}
        config_data['WowFolder'] = self.result

        with open('config.json', 'w+') as f:
            f.write(json.dumps(config_data))
        
        f.close()
        self.master.destroy()

    def directory_callback(self, var_name, var_index, operation):
        self.result = self.directory_textbox.get()
        if self.result:
            self.next_button.config(state="normal")
        else:
            self.next_button.config(state="disabled")
    
    def location_screen(self):
        location_label = Label(self.master, text="Please select the location of your World of Warcraft installation.")
        location_label.grid(row=0, columnspan=2, pady=10)

        directory_button = Button(self.master, text="Select Folder", command = self.select_callback)
        directory_button.grid(row=1, column=0, sticky=E, padx=5)

        self.directory_string = StringVar()
        self.directory_string.trace_add("write", self.directory_callback)

        self.directory_textbox = Entry(self.master, width=48, textvariable=self.directory_string)
        self.directory_textbox.grid(row=1, column=1, sticky=W, pady=30)

        self.next_button = Button(self.master, text="Next", command = self.next_callback, state="disabled")
        self.next_button.grid(row=2, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    SetupWizard()