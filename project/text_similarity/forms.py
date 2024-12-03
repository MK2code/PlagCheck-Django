# text_similarity/forms.py
from django import forms
from file_manager.models import Folder

class FolderSelectionForm(forms.Form):
    folders = forms.ModelMultipleChoiceField(
        queryset=Folder.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Folders"
    )

    def __init__(self,owner, *args, **kwargs):
        super(FolderSelectionForm, self).__init__(*args, **kwargs)
        self.fields['folders'].queryset = Folder.objects.filter(owner=owner)
        self.fields['folders'].label_from_instance = self.get_label_from_instance

    def get_label_from_instance(self, obj):
        return f"{obj.name} (No. of files = {obj.file_set.count()})"
