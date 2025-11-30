from django import forms
from .models import About, Content, Home
from django_ckeditor_5.widgets import CKEditor5Widget
import datetime

class AboutForm(forms.ModelForm):
    mission = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="Mission statement"
    )
    vision = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="Vision statement"
    )
    history = forms.CharField(
        required=False,
        widget=CKEditor5Widget(config_name='default'),
        help_text="Organization history (optional)"
    )
    description = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="General description"
    )
    address = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="Complete address"
    )
    working_hours = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="e.g., Mon-Fri: 8:00 AM - 4:30 PM"
    )

    is_active = forms.BooleanField(
        required=False,
        label="Active/Published",
        help_text="Check to mark this About entry as active/published."
    )

    class Meta:
        model = About
        fields = ['title', 'mission', 'vision', 'history', 'description', 'established_year', 'phone', 'email', 'address', 'working_hours', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +123-456-7890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@healthcenter.com'}),
            'established_year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 1990'}),
        }

    def clean_established_year(self):
        """Validate established year is reasonable"""
        year = self.cleaned_data.get('established_year')
        if year:
            current_year = datetime.datetime.now().year
            if year < 1800:
                raise forms.ValidationError('Established year cannot be before 1800.')
            if year > current_year:
                raise forms.ValidationError(f'Established year cannot be in the future (current year: {current_year}).')
        return year

    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove common separators for validation
            cleaned = phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')
            if not cleaned.isdigit():
                raise forms.ValidationError('Phone number should contain only numbers and separators (-, +, spaces, parentheses).')
        return phone

    def clean_title(self):
        """Validate title length and content"""
        title = self.cleaned_data.get('title')
        if title:
            if len(title) < 3:
                raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    
class ContentForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditor5Widget(config_name='default'),
        help_text="Content body"
    )

    class Meta:
        model = Content
        fields = ['heading', 'body']
        widgets = {
            'heading': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter heading'}),
        }

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class HomeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save', css_class='btn btn-primary mt-3'))

    class Meta:
        model = Home
        fields = [
            'banner_title', 'banner_image_1', 'banner_image_2', 'banner_image_3',
            'banner_description_1', 'banner_description_2', 'banner_description_3',
            'welcome_message', 'short_description', 'vision', 'mission', 'image', 'video_embed'
        ]
        widgets = {
            'banner_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter banner title'}),
            'banner_description_1': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Banner description 1'}),
            'banner_description_2': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Banner description 2'}),
            'banner_description_3': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Banner description 3'}),
        }