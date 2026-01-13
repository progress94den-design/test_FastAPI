from sqlalchemy import select
from sqlalchemy.sql import Select

from crud.base import CRUDBase
from models.article import Article


class CRUDArticle(CRUDBase[Article]):
    def __init__(self):
        super().__init__(Article)

    def get_list_smtp(self) -> Select:
        stmt = select(self.model).order_by(self.model.created_at.desc())
        return stmt
