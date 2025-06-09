from exception.entity_not_found_exception import EntityNotFoundException


class FileNotFoundException(EntityNotFoundException):
    status_code = 404
    detail = "File not found"
