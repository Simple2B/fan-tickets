from pydantic import BaseModel


class NotificationNewUserRegistered(BaseModel):
    username: str


class NotificationUserActivated(BaseModel):
    email: str
