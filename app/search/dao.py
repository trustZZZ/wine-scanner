from app.dao.base import BaseDAO
from app.search.models import Search


class SearchDAO(BaseDAO):
    model = Search
