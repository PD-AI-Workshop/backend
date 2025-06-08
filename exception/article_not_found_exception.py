from exception.entity_not_found_exception import EntityNotFoundException


class ArticleNotFoundException(EntityNotFoundException):
    status_code = 404
    detail = "Article not found"
