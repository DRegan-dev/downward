from django import forms
from .models import DescentType, Ritual

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

class RitualForm(forms.ModelForm):
    class Meta:
        model = Ritual
        fields = ['name', 'description', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'admin-form-input',
                'placeholder': 'Enter ritual name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'admin-form-input',
                'rows': 3,
                'placeholder': 'Describe this ritual'
            }),
            'type': forms.Textarea(attrs={
                'class': 'admin-form-input'
            })

        }