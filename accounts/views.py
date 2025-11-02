from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


def auth_slider(request):
    """Trang đăng nhập & đăng ký (chung giao diện)"""
    login_form = AuthenticationForm()
    register_form = UserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Chào mừng {user.username} quay lại!")
                return redirect('forum:post_list')
            else:
                messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")

        elif 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Tạo tài khoản thành công! Hãy đăng nhập.")
                return redirect('login')
            else:
                messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")

    return render(request, 'registration/auth_slider.html', {
        'login_form': login_form,
        'register_form': register_form,
    })
