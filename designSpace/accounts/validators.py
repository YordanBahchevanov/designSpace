from functools import partial

from django.core.exceptions import ValidationError


def validate_name(value, field_name):
    """Validator to ensure name starts with uppercase letter and contains only alphabetic characters."""
    if not value.isalpha():
        raise ValidationError(f"{field_name} must contain only letters.")

    if not value[0].isupper():
        raise ValidationError(f"{field_name} must start with an uppercase letter.")

validate_first_name = partial(validate_name, field_name="First name")
validate_last_name = partial(validate_name, field_name="Last name")