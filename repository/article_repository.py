from model.article import Article
from repository.crud_base_repository import CRUDBaseRepository


class ArticleRepository(CRUDBaseRepository):
    model = Article
