from django.core.exceptions import ValidationError


class ValidateFileTypeMixin:
    valid_extensions = ['.jpg', '.jpeg']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_file_type(self, file):
        if not file:
            return file

        if hasattr(file, 'public_id'):
            return file

        if hasattr(file, 'name') and not any(file.name.lower().endswith(ext) for ext in self.valid_extensions):
            raise ValidationError("Only JPEG files are allowed.")

        return file