class MappingException(Exception):
    """Base exception for mapping errors."""
    pass

class InvalidMapException(MappingException):
    """Raised when a value cannot be found in enum."""
    pass

class InvalidBlockException(MappingException):
    """Raised when a value cannot be converted to a valid block."""
    pass

class InvalidConversionException(MappingException):
    """Raised when a value cannot be converted to another data type."""
    pass

class InvalidDateException(MappingException):
    """Raised when a value cannot be converted to a valid date."""
    pass

class DateOverflowException(MappingException):
    """Raised when the mapped date value exceeds the byte limit."""
    pass

class StorageException(Exception):
    """Base exception for storage errors."""
    pass