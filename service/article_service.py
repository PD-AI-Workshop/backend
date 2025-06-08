from mapper.article_mapper import ArticleMapper
from repository.article_repository import ArticleRepository
from exception.article_not_found_exception import ArticleNotFoundException
from dto.article_dto import ArticleDto, CreateArticleDto, UpdateArticleDto


class ArticleService:
    def __init__(self, repository: ArticleRepository, mapper: ArticleMapper):
        self.mapper = mapper
        self.repository = repository

    async def get_all(self) -> list[ArticleDto]:
        articles = await self.repository.get_all()
        return [self.mapper.to_dto(dto_model=ArticleDto, orm_model=article) for article in articles]

    async def get_by_id(self, id: int) -> ArticleDto:
        article = await self.repository.get_by_id(id)

        if not (article):
            raise ArticleNotFoundException()

        return self.mapper.to_dto(dto_model=ArticleDto, orm_model=article)

    async def create(self, dto: CreateArticleDto) -> ArticleDto:
        article_dict = self.mapper.to_dict(dto)
        created_article = await self.repository.create(article_dict)
        return self.mapper.to_dto(orm_model=created_article, dto_model=ArticleDto)

    async def update(self, id: int, dto: UpdateArticleDto) -> None:
        article_dict = self.mapper.to_dict(dto)
        await self.repository.update(id=id, article_dict=article_dict)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)
