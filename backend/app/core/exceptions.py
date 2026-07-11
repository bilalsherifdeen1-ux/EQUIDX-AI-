"""Domain-level exceptions. Kept free of any HTTP/framework concerns so the
domain and application layers never import FastAPI — the API layer is
responsible for translating these into HTTP responses (see
app/api/v1/error_handlers.py)."""


class EquidxError(Exception):
    """Base class for all application errors."""


class NotFoundError(EquidxError):
    pass


class AlreadyExistsError(EquidxError):
    pass


class UnauthorizedError(EquidxError):
    pass


class ForbiddenError(EquidxError):
    pass


class ValidationError(EquidxError):
    pass
