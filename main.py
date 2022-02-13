import json
import threading
import time

from sync_controller import SyncController
from sync_model import SyncModel
from sync_view import SyncView
from wizard import SetupWizard

is_ready = False


def initial_sync():
    global is_ready
    controller.init_sync()
    is_ready = True


def sync():
    if is_ready:
        controller.update_addons()
    time.sleep(30)
    sync()


def update_view():
    if is_ready:
        view.update()
    time.sleep(10)
    update_view()


try:
    f = open("config.json", "r")
    config_data = json.load(f)
except:
    SetupWizard()

model = SyncModel()
controller = SyncController(model)
view = SyncView(controller, model)

model.register_observer(view)

initial_sync_thread = threading.Thread(target=initial_sync)
initial_sync_thread.start()
sync_thread = threading.Thread(target=sync)
sync_thread.start()
view_update_thread = threading.Thread(target=update_view)
view_update_thread.start()

view.start_tkinter()
