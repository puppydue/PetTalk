from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, PetProfile
from .forms import UserProfileForm, PetProfileForm

@login_required
def my_profile(request):
    # tạo profile trống cho user mới đăng ký
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    pets = PetProfile.objects.filter(user=request.user).order_by("created_at")

    saved_user = request.GET.get("saved_user") == "1"
    saved_pet_id = request.GET.get("saved_pet")
    added_pet = request.GET.get("added_pet") == "1"

    # form thông tin cá nhân (không update username; chỉ update first_name/last_name/email + UserProfile)
    if request.method == "POST" and request.POST.get("form_name") == "user_form":
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            u: User = request.user
            u.first_name = request.POST.get("first_name", u.first_name)
            u.last_name  = request.POST.get("last_name",  u.last_name)
            u.email      = request.POST.get("email",      u.email)
            u.save()
            url = reverse("profiles:my_profile") + "?saved_user=1#user-form"
            return redirect(url)
    else:
        form = UserProfileForm(instance=profile)

    # form thêm pet (trống)
    add_pet_form = PetProfileForm(prefix="new")

    # ghép (pet, form) để template lặp không cần truy cập dict phức tạp
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
            # ✅ dùng messages thay vì query string
            messages.success(request, "✅ Đã thêm thú cưng thành công!")
            return redirect("profiles:my_profile")
    return redirect("profiles:my_profile")

@login_required
def pet_update(request, pk):
    pet = get_object_or_404(PetProfile, pk=pk, user=request.user)
    if request.method == "POST" and request.POST.get("form_name") == f"pet_form_{pk}":
        form = PetProfileForm(request.POST, request.FILES, instance=pet, prefix=f"pet{pk}")
        if form.is_valid():
            form.save()
            url = reverse("profiles:my_profile") + f"?saved_pet={pk}#pet-{pk}"
            return redirect(url)
    return redirect("profiles:my_profile")
