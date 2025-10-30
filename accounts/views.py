from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomLoginForm, CustomRegisterForm
from django.contrib.auth.models import Group

def auth_slider(request):
    """Trang đăng nhập / đăng ký (chung giao diện)"""
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = CustomLoginForm(request, data=request.POST)
            register_form = CustomRegisterForm()
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Chào mừng {user.username}!")
                return redirect('forum:post_list')
            else:
                messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
        elif 'register' in request.POST:
            register_form = CustomRegisterForm(request.POST)
            login_form = CustomLoginForm()
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.save()
                # Thêm mặc định vào nhóm "User"
                group, created = Group.objects.get_or_create(name='User')
                user.groups.add(group)
                messages.success(request, "Đăng ký thành công! Hãy đăng nhập.")
                return redirect('login')
            else:
                messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")
    else:
        login_form = CustomLoginForm()
        register_form = CustomRegisterForm()
    return render(request, 'accounts/auth_slider.html', {
        'login_form': login_form,
        'register_form': register_form,
    })

@login_required
def home(request):
    return render(request, 'forum:post_list')

def logout_view(request):
    logout(request)
    messages.success(request, "Bạn đã đăng xuất thành công.")
    return redirect('login')

def forgot_password(request):
    """Dùng PasswordResetForm có sẵn của Django"""
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                email_template_name='accounts/reset_email.html',
            )
            messages.success(request, "Liên kết đặt lại mật khẩu đã được gửi đến email của bạn.")
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'accounts/forgot_password.html', {'form': form})
