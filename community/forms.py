from django import forms
from .models import Contents
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class Writing_contents(forms.ModelForm):
    class Meta:
        model = Contents
        fields = ['제목', '내용']

        widgets = {
            '제목': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width: 837px', 'placeholder': '제목을 입력하세요.'}
            ),
            '내용': forms.CharField(widget=CKEditorUploadingWidget()),
        }
