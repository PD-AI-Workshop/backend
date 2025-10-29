import pytest
import json
from redis import Redis
from unittest.mock import Mock

from service.article_service import ArticleService
from repository.article_repository import ArticleRepository
from mapper.article_mapper import ArticleMapper
from dto.article_dto import ArticleDto, UpdateArticleDto
from model.user import User
from model.article import Article
from repository.user_repository import UserRepository
from exception.article_not_found_exception import ArticleNotFoundException

from tests.core.data.dto.article_factory import ArticleDTOFactory


class TestArticleServicePositive:
    """Тесты для ArticleService - проверяем бизнес-логику работы со статьями (Позитивыне проверки)"""

    @pytest.mark.asyncio
    async def test_get_all(
        self,
        article_service: ArticleService,
        mock_redis_client: Redis,
        article_mock_repository: ArticleRepository,
        article_mock_mapper: ArticleMapper,
    ):
        """
        Тест получения всех статей когда кэш пустой.
        Сценарий: запросить данные из БД, преобразовать в DTO, сохранить в кэш.
        """
        ARTICLE_COUNT = 2
        expected_dto = ArticleDTOFactory.dto_list(count=ARTICLE_COUNT)
        orm_articles = [Mock(**dto.model_dump()) for dto in expected_dto]

        mock_redis_client.get.return_value = None
        article_mock_repository.get_all.return_value = orm_articles
        article_mock_mapper.to_dto.side_effect = expected_dto

        result = await article_service.get_all()

        assert result == expected_dto
        mock_redis_client.get.assert_called_once()
        article_mock_repository.get_all.assert_called_once()
        assert article_mock_mapper.to_dto.call_count == ARTICLE_COUNT
        article_mock_mapper.to_dto.assert_any_call(orm_model=orm_articles[0], dto_model=ArticleDto)
        mock_redis_client.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_all_cached(self, article_service: ArticleService, mock_redis_client: Redis):
        """
        Тест получения всех статей когда данные есть в кэше.
        Сценарий: вернуть данные из кэша, НЕ обращаться к БД.
        """
        expected_dto = ArticleDTOFactory.dto_list()
        redis_articles_json = json.dumps([dto.model_dump_json() for dto in expected_dto])

        mock_redis_client.get.return_value = redis_articles_json

        result = await article_service.get_all()

        assert result == expected_dto
        mock_redis_client.get.assert_called_once()
        mock_redis_client.set.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_by_id(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        article_mock_mapper: ArticleMapper,
        user_mock_repository: UserRepository,
        sample_article_dto: ArticleDto,
        mock_redis_client: Redis,
        user: User,
        article: Article,
    ):
        """
        Тест получения статьи по ID когда кэш пустой.
        Сценарий: запросить статью из БД, получить пользователя, преобразовать в DTO, сохранить в кэш.
        """
        mock_redis_client.get.return_value = None
        article_mock_repository.get_by_id.return_value = article
        article_mock_mapper.to_dto.return_value = sample_article_dto
        user_mock_repository.get_user_by_id.return_value = user

        result = await article_service.get_by_id(id=sample_article_dto.id)

        assert result == sample_article_dto
        mock_redis_client.get.assert_called_once_with(f"article:{sample_article_dto.id}")
        article_mock_repository.get_by_id.assert_called_once_with(id=sample_article_dto.id)
        user_mock_repository.get_user_by_id.assert_called_once_with(id=sample_article_dto.user_id)
        article_mock_mapper.to_dto.assert_called_once()
        mock_redis_client.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_by_id_cached(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        sample_article_dto: ArticleDto,
        mock_redis_client: Redis,
    ):
        """
        Тест получения статьи по ID когда данные есть в кэше.
        Сценарий: вернуть данные из кэша, НЕ обращаться к БД и репозиториям.
        """
        redis_article_json = sample_article_dto.model_dump_json()

        mock_redis_client.get.return_value = redis_article_json

        result = await article_service.get_by_id(sample_article_dto.id)

        assert result == sample_article_dto
        mock_redis_client.get.assert_called_once()
        assert article_mock_repository.get_by_id.call_count == 0

    @pytest.mark.asyncio
    async def test_create(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        article_mock_mapper: ArticleMapper,
        user: User,
    ):
        """
        Тест создания новой статьи.
        Сценарий: преобразовать DTO в словарь, сохранить в БД, вернуть созданную статью как DTO.
        """
        create_article_dto = ArticleDTOFactory.create_dto()
        created_article_dto = ArticleDTOFactory.dto(**create_article_dto.model_dump())
        orm_created_article = created_article_dto.model_dump()
        orm_created_article.update({"user_id": user.id})

        article_mock_mapper.to_dict.return_value = create_article_dto.model_dump()
        article_mock_repository.create.return_value = orm_created_article
        article_mock_mapper.to_dto.return_value = created_article_dto

        result = await article_service.create(dto=create_article_dto, user=user)

        assert result == created_article_dto
        article_mock_mapper.to_dict.assert_called_once_with(dto_model=create_article_dto)
        article_mock_repository.create.assert_called_once()
        article_mock_mapper.to_dto.assert_called_once_with(orm_model=orm_created_article, dto_model=ArticleDto)

    @pytest.mark.asyncio
    async def test_update(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        mock_redis_client: Redis,
        article_mock_mapper: ArticleMapper,
        sample_update_dto: UpdateArticleDto,
        user: User,
    ):
        """
        Тест обновления статьи.
        Сценарий: преобразовать DTO в словарь, обновить в БД, инвалидировать кэш.
        """
        orm_article = sample_update_dto.model_dump()
        article_mock_mapper.to_dict.return_value = orm_article

        await article_service.update(1, sample_update_dto, user)

        article_mock_mapper.to_dict.assert_called_once_with(sample_update_dto)
        article_mock_repository.update.assert_called_once()
        assert mock_redis_client.delete.call_count == 2

    @pytest.mark.asyncio
    async def test_delete(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        mock_redis_client: Redis,
    ):
        """
        Тест удаления статьи.
        Сценарий: удалить статью из БД, инвалидировать кэш.
        """
        await article_service.delete(1)

        article_mock_repository.delete.assert_called_once_with(id=1)
        assert mock_redis_client.delete.call_count == 2


class TestArticleServiceNegative:
    """Тесты для ArticleService - проверяем бизнес-логику работы со статьями (Негативные проверки)"""

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        article_service: ArticleService,
        article_mock_repository: ArticleRepository,
        mock_redis_client: Redis,
    ):
        """
        Тест получения несуществующей статьи по ID.
        Сценарий: запросить статью из БД, получить пустое значение, выбросить исключение ArticleNotFoundException.
        """
        mock_redis_client.get.return_value = None
        article_mock_repository.get_by_id.return_value = None

        with pytest.raises(ArticleNotFoundException):
            await article_service.get_by_id(999)

        mock_redis_client.get.assert_called_once()
        article_mock_repository.get_by_id.assert_called_once_with(999)
