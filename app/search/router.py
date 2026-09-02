from fastapi import APIRouter
from app.search.schemas import SSearchList

router = APIRouter(
    prefix="/search",
    tags=["/Search"]
)

# Поиск по пользовательским данным данным
@router.get("/search")
def search(search_list: SSearchList):
    pass
