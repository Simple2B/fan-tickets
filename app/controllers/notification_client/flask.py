from flask_sse import sse


from .notification import NotificationClient


class FlaskSSENotification(NotificationClient):
    def send_notification(
        self,
        data: dict,
        channel: str,
    ):
        sse.publish(data, channel=channel)
