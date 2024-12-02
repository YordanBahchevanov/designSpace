from datetime import datetime
from django import forms
from django.forms import modelformset_factory

from .models import Project, ProjectImage


class ProjectCreateForm(forms.ModelForm):
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

    def clean_year(self):
        year = self.cleaned_data.get("year")
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year):
            raise forms.ValidationError(f"Year must be between 1900 and {current_year}.")
        return year

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ("image",)


ProjectImageFormSet = modelformset_factory(
    ProjectImage,
    fields=('image',),
    extra=5,
)
