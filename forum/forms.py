from django import forms
from .models import Post, Comment, ReportsPost


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'topic', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tiêu đề bài viết...'}),
            'topic': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Chia sẻ điều gì đó...'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Viết bình luận...', 'class': 'form-control'})
        }


class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportsPost
        fields = ['reason', 'details']
        widgets = {
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lý do báo cáo'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Chi tiết (nếu có)...'}),
        }
