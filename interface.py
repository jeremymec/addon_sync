from updater import push_addons_to_git
from copy_addons import copy_addons
from tkinter import messagebox, Tk, Menu
from updater import push_addons_to_git
from tkinter.filedialog import askdirectory
from notify import NotificationSender
import threading
import json

class Interface:

    def __init__(self):
        self.master = Tk()
        self.master.minsize(400, 300)
        self.master.title("Addon Sync")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.trayMenu = None
        sync_thread = threading.Thread(target=self.upstream_sync)
        sync_thread.start()
        self.notifcation_sender = NotificationSender()
        self.master.mainloop()

    def read_config(self):
        f = open('config.json', 'r') 
        config_data = json.load(f)
        self.path_to_wow = config_data['WowFolder']

    def upstream_sync(self):
        copy_addons(self.path_to_wow)
        push_addons_to_git()
        print("Hello I am here")
        self.notifcation_sender.create_notification()
    
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
