import json, time, threading
from wizard import SetupWizard
from sync_model import SyncModel
from sync_view import SyncView
from sync_controller import SyncController

is_ready = False

def initial_sync():
    global is_ready
    controller.init_sync()
    is_ready = True

def sync_on_timer():
    global is_ready
    while(is_ready):
        controller.update_addons()
        time.sleep(30)

def update_view():
    global is_ready
    while(is_ready):
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

initial_sync_thread = threading.Thread(target=initial_sync)
initial_sync_thread.start()
sync_thread = threading.Thread(target=sync_on_timer)
sync_thread.start()
view_update_thread = threading.Thread(target=update_view)
view_update_thread.start()

view.start_tkinter()