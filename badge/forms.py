from django import forms
from .models import Badge

class BadgeForm(forms.ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'description', 'type', 'target', 'color', 'achieved_count']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên danh hiệu...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Mô tả ngắn về danh hiệu...'
            }),
            'type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'target': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'placeholder': 'Nhập mục tiêu cần đạt...'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'achieved_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
        }

        labels = {
            'name': 'Tên danh hiệu',
            'description': 'Mô tả',
            'type': 'Loại danh hiệu',
            'target': 'Mục tiêu cần đạt',
            'color': 'Màu hiển thị',
            'achieved_count': 'Số người đã đạt',
        }
