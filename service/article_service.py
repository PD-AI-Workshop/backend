import json
from redis import Redis
from mapper.article_mapper import ArticleMapper
from model.user import User
from repository.article_repository import ArticleRepository
from exception.article_not_found_exception import ArticleNotFoundException
from dto.article_dto import ArticleDto, CreateArticleDto, UpdateArticleDto
from repository.user_repository import UserRepository


class ArticleService:
    def __init__(
        self, repository: ArticleRepository, user_repository: UserRepository, mapper: ArticleMapper, redis_client: Redis
    ):
        self.mapper = mapper
        self.repository = repository
        self.redis_client = redis_client
        self.user_repository = user_repository

    async def get_all(self) -> list[ArticleDto]:
        cache_key = "articles:all"
        cached = self.redis_client.get(cache_key)

        if cached:
            return [ArticleDto.model_validate_json(article) for article in json.loads(cached)]

        articles = await self.repository.get_all()
        result = [self.mapper.to_dto(dto_model=ArticleDto, orm_model=article) for article in articles]
        serialized = json.dumps([article.model_dump_json() for article in result])

        self.redis_client.set(cache_key, serialized, ex=86400)

        return result

    async def get_by_id(self, id: int) -> ArticleDto:
        cache_key = f"article:{id}"
        cached = self.redis_client.get(cache_key)

        if cached:
            return ArticleDto.model_validate_json(cached)

        article = await self.repository.get_by_id(id)

        if not (article):
            raise ArticleNotFoundException()

        user = await self.user_repository.get_user_by_id(article.user_id)
        dto = self.mapper.to_dto(dto_model=ArticleDto, orm_model=article)
        dto.username = user.username if user else None
        self.redis_client.set(cache_key, dto.model_dump_json(), ex=86400)
        return dto

    async def create(self, dto: CreateArticleDto, user: User) -> ArticleDto:
        article_dict = self.mapper.to_dict(dto)
        article_dict["user_id"] = user.id
        created_article = await self.repository.create(article_dict)

        self.redis_client.delete("articles:all")
        return self.mapper.to_dto(orm_model=created_article, dto_model=ArticleDto)

    async def update(self, id: int, dto: UpdateArticleDto, user: User) -> None:
        article_dict = self.mapper.to_dict(dto)
        article_dict["user_id"] = user.id

        await self.repository.update(id=id, article_dict=article_dict)
        self.redis_client.delete(f"article:{id}")
        self.redis_client.delete("articles:all")

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)
        self.redis_client.delete(f"article:{id}")
        self.redis_client.delete("articles:all")
