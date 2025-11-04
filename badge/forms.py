from django import forms
from .models import Badge

class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'achieved_count']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'achieved_count': forms.NumberInput(attrs={'class': 'form-control'}),
        }
