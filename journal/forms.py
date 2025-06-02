from django import forms
from .models import DescentType

class DescentTypeForm(forms.ModelForm):
    class Meta:
        model = DescentType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'admin-form-input',
                'rows': 3,
                'placeholder': 'Enter descent type name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'admin-form-input',
                'rows': 3,
                'placeholder': 'Describe this descent type'
            })
        }