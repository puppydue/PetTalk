from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _  # Cần import cái này


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Tên người dùng',
            'class': 'input-field'
        })
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu',
            'class': 'input-field'
        })
    )

    # Dịch lỗi "Please enter a correct username and password."
    error_messages = {
        'invalid_login': _(
            "Tên đăng nhập hoặc mật khẩu không đúng. Vui lòng thử lại."
        ),
        'inactive': _("Tài khoản này không hoạt động."),
    }


class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'placeholder': 'Tên người dùng',
            'class': 'input-field'
        }),
        # Dịch lỗi "A user with that username already exists."
        error_messages={
            'unique': _("Tên người dùng này đã tồn tại. Vui lòng chọn tên khác."),
        }
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Mật khẩu',
            'class': 'input-field'
        })
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nhập lại mật khẩu',
            'class': 'input-field'
        }),
        # Dịch lỗi "The two password fields didn’t match."
        error_messages={
            'password_mismatch': _("Mật khẩu nhập lại không khớp."),
        }
    )

    class Meta:
        model = User
        fields = ['username']  # Chỉ cần username ở đây, password sẽ được xử lý riêng

    # Bạn cũng có thể thêm các thông báo lỗi cho mật khẩu ở đây
    # Ghi đè phương thức clean_password2 để kiểm tra và trả về lỗi tùy chỉnh
    def clean_password2(self):
        password_1 = self.cleaned_data.get("password1")
        password_2 = self.cleaned_data.get("password2")
        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError(
                "Mật khẩu nhập lại không khớp.",
                code='password_mismatch'  # Mã này khớp với error_messages ở trên
            )
        return password_2

    # Django tự động validate các lỗi mật khẩu khác
    # (quá ngắn, quá phổ biến, v.v.)
    # Để dịch chúng, bạn cần cấu hình trong file settings.py
    # nhưng cách trên là đủ cho các lỗi cơ bản rồi.
