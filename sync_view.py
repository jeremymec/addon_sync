from tkinter import messagebox, Tk, Menu, Label
from tkinter.filedialog import askdirectory
import timeago
from datetime import datetime

class SyncView:

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.trayMenu = None
        
        self.master = Tk()
        self.master.minsize(400, 300)
        self.master.title("Addon Sync")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.status_label = Label(self.master, text = '')
        self.status_label.grid(row=0)

        self.last_checked_label = Label(self.master, text = '')
        self.last_checked_label.grid(row=1)

        self.update()


    def start_tkinter(self):
        self.master.mainloop()

    def update(self):
        self.status_label.config(text=self.model.get_status())

        last_checked_time = self.model.get_last_checked()
        last_checked_time_text = ''
        if last_checked_time == None:
            last_checked_time_text = 'Addons have not been synced yet'
        else:
            human_last_checked_time = timeago.format(last_checked_time, datetime.now())
            last_checked_time_text = 'Last checked ' + human_last_checked_time

        self.last_checked_label.config(text=last_checked_time_text)
    
    def on_closing(self):
        if not self.trayMenu:

            self.master.withdraw()

            self.master.tk.call('package', 'require', 'Winico')
            icon = self.master.tk.call('winico', 'createfrom', 'smiley.ico')
            self.master.tk.call('winico', 'taskbar', 'add', icon,
                        '-callback', (self.master.register(self.menu_func), '%m', '%x', '%y'),
                        '-pos', 0,
                        '-text', u'Addon Sync')

            self.trayMenu = Menu(self.master, tearoff=False)
            self.trayMenu.add_command(label="Show Window", command=self.master.deiconify)

            self.trayMenu.add_command(label="Quit", command=self.master.destroy)

        else:
            self.master.withdraw()

    def menu_func(self, event, x, y):
        if event == 'WM_RBUTTONDOWN':
            self.trayMenu.tk_popup(x, y)
        if event == 'WM_LBUTTONDOWN':
            self.master.deiconify()
