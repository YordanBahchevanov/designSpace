from django import forms

from designSpace.folders.models import Folder


class FolderCreateForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('title',)


class AddProjectToFolderForm(forms.Form):
    folder = forms.ModelChoiceField(
        queryset=Folder.objects.none(),
        required=False
    )

    new_folder_title = forms.CharField(
        max_length=100,
        required=False
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)

        if user:

            self.fields['folder'].queryset = Folder.objects.filter(user=user)

    def clean(self):
        cleaned_data = super().clean()
        folder = cleaned_data.get('folder')
        new_folder_title = cleaned_data.get('new_folder_title')

        if not folder and not new_folder_title:
            raise forms.ValidationError("You must select a folder or provide a new folder title.")

        return cleaned_data