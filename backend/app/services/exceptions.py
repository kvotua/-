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
    """Raised when node is not found"""

    pass


class NodeCannotBeDeletedError(ServiceError):
    """Raised when node is cannot be deleted"""

    pass


class NodeInDifferentTreeError(ServiceError):
    """Raised when trying reparent node to another tree"""

    pass


class AttributeTypeNotFoundError(ServiceError):
    """Raised when attribute type does not exist"""

    pass


class NodeAttributeNotFoundError(ServiceError):
    """Raised when node attribute does not exist"""

    pass


class AttributeDoesNotExistError(ServiceError):
    """Raised when type does not contain given attribute"""

    pass


class AttributeTypeAlreadyExists(ServiceError):
    """Raised when attribute type already exist exist"""

    pass


class InvalidAttributeValueError(ServiceError):
    """Raised when attribute is being passed with wrong value"""

    pass
