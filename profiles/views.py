from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, PetProfile
from .forms import UserProfileForm, PetProfileForm
from forum.models import Post, Comment


@login_required
def my_profile(request):
    # Tạo profile trống cho user mới đăng ký
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    pets = PetProfile.objects.filter(user=request.user).order_by("created_at")

    saved_user = request.GET.get("saved_user") == "1"
    saved_pet_id = request.GET.get("saved_pet")
    added_pet = request.GET.get("added_pet") == "1"

    # ======= CẬP NHẬT THÔNG TIN CÁ NHÂN =======
    if request.method == "POST" and request.POST.get("form_name") == "user_form":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            u: User = request.user
            u.first_name = request.POST.get("first_name", u.first_name)
            u.last_name = request.POST.get("last_name", u.last_name)
            u.email = request.POST.get("email", u.email)
            u.save()

            # ✅ Hiển thị popup “Lưu thông tin thành công”
            messages.success(request, "💾 Lưu thông tin cá nhân thành công!")
            url = reverse("profiles:my_profile") + "?saved_user=1"
            return redirect(url)

    else:
        form = UserProfileForm(instance=profile)

    # ======= FORM THÊM PET TRỐNG =======
    add_pet_form = PetProfileForm(prefix="new")

    # ======= GHÉP PET + FORM =======
    pet_form_pairs = []
    for p in pets:
        f = PetProfileForm(instance=p, prefix=f"pet{p.id}")
        pet_form_pairs.append((p, f))

    ctx = {
        "user_info": profile,
        "form": form,
        "add_pet_form": add_pet_form,
        "pet_form_pairs": pet_form_pairs,
        "saved_user": saved_user,
        "saved_pet_id": saved_pet_id,
        "added_pet": added_pet,
        # "posts": posts,
        # "comments": comments,
        # "posts_count": posts.count(),
        # "comments_count": comments.count(),
    }
    return render(request, "profiles/profile_detail.html", ctx)


@login_required
def pet_create(request):
    if request.method == "POST" and request.POST.get("form_name") == "new_pet_form":
        form = PetProfileForm(request.POST, request.FILES, prefix="new")
        if form.is_valid():
            pet = form.save(commit=False)
            pet.user = request.user
            pet.save()
            messages.success(request, "🐾 Đã thêm thú cưng thành công!")
            return redirect("profiles:my_profile")
    return redirect("profiles:my_profile")


@login_required
def pet_update(request, pk):
    pet = get_object_or_404(PetProfile, pk=pk, user=request.user)
    if request.method == "POST" and request.POST.get("form_name") == f"pet_form_{pk}":
        form = PetProfileForm(request.POST, request.FILES, instance=pet, prefix=f"pet{pk}")
        if form.is_valid():
            form.save()
            # ✅ Thêm thông báo popup
            messages.success(request, "💾 Lưu thông tin thú cưng thành công!")
            return redirect("profiles:my_profile")
    return redirect("profiles:my_profile")
