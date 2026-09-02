from sqlalchemy import Column, Integer, String,DateTime
from app.database import Base


class Messages(Base):
    __tablename__ = "messages"

    chat_id = Column(Integer, primary_key=True, nullable=True)
    user_id = Column(Integer, nullable=True)
    bot_answers = Column(String, nullable=True)
    user_messages = Column(String, nullable=True)
    data = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}