from win10toast import ToastNotifier

class NotificationSender:

    def __init__(self):
        self.toaster = ToastNotifier()

    def create_notification(self):
        self.toaster.show_toast("Sample Notification","Python is awesome!!!")