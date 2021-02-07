from win10toast import ToastNotifier


class NotificationSender:
    def __init__(self):
        self.toaster = ToastNotifier()

    def create_notification(self, title, body):
        self.toaster.show_toast(title, body, threaded=True)
