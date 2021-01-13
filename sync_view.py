from tkinter import messagebox, Tk, Menu, Label, Toplevel, Button, Frame
from tkinter.filedialog import askdirectory
import timeago
from datetime import datetime
from sync_model import Status, SyncEventType
from sync_view_style import ROW_PADDING, COLUMN_PADDING

class SyncView:

    def __init__(self, controller, model):
        self.controller = controller
        self.model = model
        self.trayMenu = None
        
        self.master = Tk()
        # self.master.minsize(400, 300)
        self.master.title("Addon Sync")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.master.grid_columnconfigure(0, minsize=COLUMN_PADDING)
        self.master.grid_columnconfigure(2, minsize=COLUMN_PADDING)
        self.master.grid_rowconfigure(0, minsize=ROW_PADDING)
        self.master.grid_rowconfigure(4, minsize=ROW_PADDING)

        self.status_label = Label(self.master, text = '', font=("Calibri", 18), width=25)
        self.status_label.grid(row=1, column=1)

        self.last_checked_label = Label(self.master, text = '')
        self.last_checked_label.grid(row=2, column=1)

        self.sync_button = Button(self.master, text='Sync', command=self.sync_button_callback)
        self.sync_button.grid(row=3, column=1)

        self.update()


    def start_tkinter(self):
        self.master.mainloop()

    def update(self):
        if self.model.get_status() == Status.CONFLICT:
            self.controller.ack_conflict()
            self.open_merge_popup()

        self.status_label.config(text=self.model.get_status())

        sync_event = self.model.get_last_sync_event()
        sync_status_text = ''

        if sync_event == None:
            last_checked_time = self.model.get_last_checked()

            if last_checked_time == None:
                sync_status_text = 'Addons have not been synced yet'
            else:
                sync_time_text = timeago.format(last_checked_time, datetime.now())
                sync_status_text = 'Last checked {sync_time}'.format(sync_time = sync_time_text)
        else:
            sync_time = sync_event.get_sync_time()

            sync_time_text = timeago.format(sync_time, datetime.now())

            sync_type = sync_event.get_sync_type()
            sync_type_text = sync_type.value

            sync_status_text = 'Last {sync_type} {sync_time}'.format(sync_type = sync_type_text, sync_time = sync_time_text)

        self.last_checked_label.config(text=sync_status_text)

    def sync_button_callback(self):
        self.controller.update_addons()
    
    def open_merge_popup(self):
        popup_win = Toplevel()
        popup_win.title = "Conflict"
        popup_win.minsize(250,100)
        message = "Merge conflict yo"
        Label(popup_win, text=message).grid(row=0, columnspan=2)
        Button(popup_win, text='Use Local', command=self.controller.resolve_conflict_with_local).grid(row=1, column=0)
        Button(popup_win, text='Use Cloud', command=self.controller.resolve_conflict_with_cloud).grid(row=1, column=1)
    
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
