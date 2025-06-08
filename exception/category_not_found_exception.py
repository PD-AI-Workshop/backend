from exception.entity_not_found_exception import EntityNotFoundException


class CategoryNotFoundException(EntityNotFoundException):
    status_code = 404
    detail = "Category not found"
