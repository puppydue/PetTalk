
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomRegisterForm, CustomLoginForm
from django.contrib import messages


def auth_slider(request):
    login_form = CustomLoginForm()
    register_form = CustomRegisterForm()

    # Biến này sẽ quyết định panel nào được hiển thị khi load trang
    active_panel = 'login'

    if request.method == 'POST':
        if 'login' in request.POST:
            active_panel = 'login'  # Người dùng submit form login
            login_form = CustomLoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"Chào mừng {user.username} quay lại!")

                # ✅ Ưu tiên redirect đến trang người dùng định vào (nếu có)
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('forum:post_list')  # fallback mặc định

        elif 'register' in request.POST:
            active_panel = 'register'  # Người dùng submit form register
            register_form = CustomRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Tạo tài khoản thành công! Hãy đăng nhập.")
                return redirect('/')
            # Không cần 'else' ở đây, form tự động chứa lỗi
            # và sẽ được render bên dưới

    return render(request, 'registration/auth_slider.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_panel': active_panel,  # Truyền biến này ra template
    })