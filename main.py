from wizard import SetupWizard
from sync_model import SyncModel
from sync_view import SyncView
from sync_controller import SyncController
import threading

wizard = SetupWizard()

model = SyncModel()
controller = SyncController(model)
view = SyncView(controller, model)

model.register_observer(view)
update_thread = threading.Thread(target=controller.sync)
update_thread.start()
view.start_tkinter()
