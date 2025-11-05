from django import forms
from django.utils import timezone
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'end_date', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tiêu đề sự kiện'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Nhập mô tả sự kiện...'
            }),
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập địa điểm tổ chức'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

    # ⚠️ Kiểm tra trùng tiêu đề — chỉ áp dụng khi tạo mới
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            return title

        # Nếu form đang chỉnh sửa (đã có instance), bỏ qua chính nó
        existing = Event.objects.filter(title__iexact=title)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError("⚠️ Tiêu đề của bạn đã tồn tại.")
        return title

    # ⚠️ Kiểm tra logic thời gian
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('date')
        end = cleaned_data.get('end_date')

        # Xóa lỗi tự động sinh từ model (tránh trùng dòng)
        self._errors.pop('end_date', None)

        if start and end and end <= start:
            raise forms.ValidationError(
                "⚠️ Thời gian kết thúc của bạn đang sớm hơn thời gian bắt đầu."
            )

        # (Tuỳ chọn) Không cho tạo sự kiện trong quá khứ
        if start and start < timezone.now():
            raise forms.ValidationError(
                "⚠️ Thời gian bắt đầu sự kiện không được ở quá khứ."
            )

        return cleaned_data
