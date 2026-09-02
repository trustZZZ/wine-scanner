from app.dao.base import BaseDAO
from app.messanger.models import Messages


class MessagesDAO(BaseDAO):
    model = Messages
