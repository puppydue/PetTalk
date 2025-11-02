from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import login
from django.contrib.auth.models import Group
from .forms import CustomLoginForm, CustomRegisterForm

# LoginView đã được khai báo trong urls.py, không cần view login tự viết nữa

def register(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Cho vào group "User" mặc định
            group, _ = Group.objects.get_or_create(name='User')
            user.groups.add(group)
            messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")
    else:
        form = CustomRegisterForm()
    # dùng lại giao diện slider, kích hoạt panel đăng ký bằng class
    return render(request, 'accounts/auth_slider.html', {
        'register_form': form,
        'activate_signup': True,
    })

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/reset_email.html',
            )
            messages.success(request, "Đã gửi liên kết đặt lại mật khẩu.")
            return redirect('accounts:login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})

# Cho LoginView dùng được form tuỳ biến
CustomLoginForm = CustomLoginForm
