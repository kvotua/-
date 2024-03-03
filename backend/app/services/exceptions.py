class ServiceError(Exception):
    """Base exception for service errors."""


class ProjectNotFoundError(ServiceError):
    """Raised when a project is not found."""


class UserNotFoundError(ServiceError):
    """Raised when a user is not found."""


class WrongInitiatorError(ServiceError):
    """Raised when initiator is not found."""


class UserExistError(ServiceError):
    """Raised when a user already exists."""


class NotAllowedError(ServiceError):
    """Raised when an action is not allowed."""

    pass


class NodeNotFoundError(ServiceError):
    pass
