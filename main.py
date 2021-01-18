import json, time, threading
from wizard import SetupWizard
from sync_model import SyncModel
from sync_view import SyncView
from sync_controller import SyncController

def sync_on_timer():
    while(True):
        controller.update_addons()
        time.sleep(60)

def update_view():
    while(True):
        time.sleep(10)
        view.update()

try:
    f = open('config.json', 'r') 
    config_data = json.load(f)
    if config_data["ValidConfig"] != "True": raise Exception
except:
    SetupWizard() 

model = SyncModel()
controller = SyncController(model)
view = SyncView(controller, model)

model.register_observer(view)

sync_thread = threading.Thread(target=sync_on_timer)
sync_thread.start()
# view_update_thread = threading.Thread(target=update_view)
# view_update_thread.start()

view.start_tkinter()
