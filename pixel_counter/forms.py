from django import forms
from .models import ImageModel


class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ['image', ]
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }
        labels = {
            'image': 'Выберите изображение из файловой системы'
        }