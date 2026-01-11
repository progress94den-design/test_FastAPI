from crud.base import CRUDBase
from models.article import Article


class CRUDArticle(CRUDBase[Article]):
    def __init__(self):
        super().__init__(Article)
