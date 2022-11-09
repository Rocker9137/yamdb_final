from django.conf import settings
from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидатор имени пользователя."""
    if value == settings.RESERVED_NAME:
        raise ValidationError(
            settings.MESSAGE_FOR_RESERVED_NAME
        )
