# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login
# from .forms import CustomRegisterForm, CustomLoginForm
# from django.contrib import messages
#
#
# def auth_slider(request):
#     login_form = CustomLoginForm()
#     register_form = CustomRegisterForm()
#
#     if request.method == 'POST':
#         if 'login' in request.POST:
#             login_form = CustomLoginForm(request, data=request.POST)
#             if login_form.is_valid():
#                 user = login_form.get_user()
#                 login(request, user)
#                 messages.success(request, f"Chào mừng {user.username} quay lại!")
#                 return redirect('forum:post_list')
#             else:
#                 messages.error(request, "Sai tên đăng nhập hoặc mật khẩu.")
#
#         elif 'register' in request.POST:
#             register_form = CustomRegisterForm(request.POST)
#             if register_form.is_valid():
#                 register_form.save()
#                 messages.success(request, "Tạo tài khoản thành công! Hãy đăng nhập.")
#                 return redirect('login')
#             else:
#                 messages.error(request, "Vui lòng kiểm tra lại thông tin đăng ký.")
#
#     return render(request, 'registration/auth_slider.html', {
#         'login_form': login_form,
#         'register_form': register_form,
#     })

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
                return redirect('forum:post_list')
            # Không cần 'else' ở đây, form tự động chứa lỗi
            # và sẽ được render bên dưới

        elif 'register' in request.POST:
            active_panel = 'register'  # Người dùng submit form register
            register_form = CustomRegisterForm(request.POST)
            if register_form.is_valid():
                register_form.save()
                messages.success(request, "Tạo tài khoản thành công! Hãy đăng nhập.")
                return redirect('login')
            # Không cần 'else' ở đây, form tự động chứa lỗi
            # và sẽ được render bên dưới

    return render(request, 'registration/auth_slider.html', {
        'login_form': login_form,
        'register_form': register_form,
        'active_panel': active_panel,  # Truyền biến này ra template
    })