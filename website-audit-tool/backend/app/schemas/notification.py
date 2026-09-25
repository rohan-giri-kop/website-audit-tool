from datetime import datetime
from pydantic import BaseModel
from datetime import datetime


class NotificationRead(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class NotificationList(BaseModel):
    total: int
    unread: int
    notifications: list[NotificationRead]