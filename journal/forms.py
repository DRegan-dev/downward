from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from .models import DescentType, DescentSession, Entry


class BaseForm(forms.ModelForm):
    """Base form class with common styling and error handling"""
    error_css_class = 'error'
    required_css_class = 'required'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form_control'
            if field.required:
                field.widget.attrs['required'] = 'required'
        
class DescentTypeForm(forms.ModelForm):
    class Meta:
        model = DescentType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter descent type name',
                'aria-label': 'Descent type name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe this descent type',
                'aria-label': 'Descent type description',
            }), 
            'type': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Select descent type',
            })
        }
        error_messages = {
            'name': {
                'required': _('Please enter a name for this descent type'),
                'max_length': _('Name is too long (maximum 100 characters)'),
            },
            'description': {
                'required': _('Please provide a description'),
            }
        }

        def clean_name(self):
            name = self.cleaned_data.get('name')
            if name and len(name.strip()) < 3:
                raise forms.ValidationError(_('Name must be at least 3 characters long'))
            return name.strip()
        
class DescentSessionForm(BaseForm):
    class Meta:
        model = DescentSession
        fields = ['descent_type', 'notes']
        widgets = {
            'descent_type': forms.Select(attrs={
                'class': 'form-select',
                'aria_label': 'Select descent type',
            }), 
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any additional notes about this session',
                'area-label': 'Session notes',
            }),
        }
        error_messages = {
            'descent_type': {
                'required': 'Please select a descent type',
            },
        }
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter active descent types
        self.fields['descent_type'].queryset = DescentType.objects.filter(
            is_active=True
        ).order_by('name')

        # Add form control class to all fields
        for field_name, field in self.fields.items():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance

class EntryForm(BaseForm):
    class Meta:
        model = Entry
        fields = ['content', 'emotion_level', 'reflection']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your thoughts and feelings...',
                'aria-label': 'Journal entry content',
            }),
            'emotion_level': forms.NumberInput(attrs={
                'class': 'form-range',
                'type': 'range',
                'min': '1',
                'max': '10',
                'step': '1',
                'aria-label': 'Emotion level',
                'oninput': 'this.nextElementSibling.value = this.value',
            }),
            'reflection': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add any refelctions or insights...',
                'aria-label': 'Reflections',
            }),
        }
        error_messages = {
            'content': {
                'required': _('Please enter some content for your journal entry'),
            },
            'emotion_level': {
                'required': _('Please rate your emotional state'),
                'min_value': _('Emotion level must be at least 1'),
                'max_value': _('Emotion level cannot be more than 10'),
            }
        }

    def clean_emotion_level(self):
        emotion_level = self.cleaned_data.get('emotion_level')
        if emotion_level is not None and (emotion_level < 1 or emotion_level > 10):
            raise forms.ValidationError(-('Emotion level must be between 1 and 10'))
        return emotion_level
    
    def clean_content(self):
        content = self.cleaned_data.get('content', '').strip()
        if len(content) < 10:
            raise forms.ValidationError(_('Please provide more details (at least 10 characters)'))
        return content
