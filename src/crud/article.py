from sqlalchemy import select, func
from sqlalchemy.sql import Select

from crud.base import CRUDBase
from models.article import Article


class CRUDArticle(CRUDBase[Article]):
    def __init__(self):
        super().__init__(Article)

    def _ts_query_simple(self, query: str):
        return func.websearch_to_tsquery("simple", query)

    def get_list_stmt(self) -> Select:
        stmt = select(self.model).order_by(self.model.created_at.desc())
        return stmt

    def search_stmt(self, *, query: str) -> Select:
        ts_query = self._ts_query_simple(query)

        stmt = (
            select(self.model)
            .where(self.model.search_vector.op("@@")(ts_query))
            .order_by(self.model.created_at.desc())
        )
        return stmt
