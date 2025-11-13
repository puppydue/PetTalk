# badge/forms.py
from django import forms
from .models import Badge

ICON_CHOICES = [
    ("🏆", "🏆 Trophy"),
    ("⭐", "⭐ Star"),
    ("🔥", "🔥 Fire"),
    ("⚡", "⚡ Lightning"),
    ("❤️", "❤️ Heart"),
    ("💬", "💬 Chat"),
    ("🚀", "🚀 Rocket"),
    ("👑", "👑 Crown"),
    ("🎁", "🎁 Gift"),
    ("🚩", "🚩 Flag"),
    ("🐱", "🐱 Meow"),
    ("🐾", "🐾 Paw"),
]

class BadgeForm(forms.ModelForm):
    icon = forms.ChoiceField(
        choices=ICON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Biểu tượng"
    )

    class Meta:
        model = Badge
        fields = ['name', 'description', 'type', 'target', 'color', 'icon', 'achieved_count']

        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'target': forms.NumberInput(attrs={'class': 'form-control'}),
            'achieved_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True
            }),
        }
