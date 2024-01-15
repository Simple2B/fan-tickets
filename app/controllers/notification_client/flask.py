from flask_sse import sse


from .notification import NotificationClient, NotificationType


class FlaskSSENotification(NotificationClient):
    def send_notification(self, data: dict, channel: str, notification_type: NotificationType):
        sse.publish(data, notification_type.value, channel=channel)
