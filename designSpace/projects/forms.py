from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

from .models import Project, ProjectImage
from ..mixins import ValidateFileTypeMixin


class ProjectCreateForm(ValidateFileTypeMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "project_type",
            "year",
            "area",
            "location",
            "cover_image",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "year": forms.NumberInput(attrs={"min": 1900, "max": datetime.now().year}),
        }

    def __init__(self, *args, **kwargs):
        self.image_formset = kwargs.pop('image_formset', None)
        super().__init__(*args, **kwargs)

    def clean_year(self):
        year = self.cleaned_data.get("year")
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year):
            raise forms.ValidationError(f"Year must be between 1900 and {current_year}.")
        return year

    def clean_cover_image(self):
        cover_image = self.cleaned_data.get('cover_image')
        return self.validate_file_type(cover_image)

    def clean(self):
        cleaned_data = super().clean()

        if self.image_formset:
            for form in self.image_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    image = form.cleaned_data.get('image')
                    if image:
                        form.validate_file_type(image)
                else:
                    raise ValidationError("Each image in the gallery must be valid.")

        return cleaned_data


class ProjectImageForm(ValidateFileTypeMixin, forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ("image",)

    def clean_gallery_image(self):
        gallery_image = self.cleaned_data.get('image')
        return self.validate_file_type(gallery_image)


ProjectImageFormSet = modelformset_factory(
    ProjectImage,
    form=ProjectImageForm,
    fields=('image',),
    extra=5,
)

class ProjectEditForm(ProjectCreateForm):
    """Edit form for updating a project."""
    pass