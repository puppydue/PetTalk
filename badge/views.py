# badge/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from .models import Badge, UserBadgeProgress
from .forms import BadgeForm
from profiles.models import UserProfile


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff or u.is_superuser)(view_func)


# =======================
# ADMIN QUẢN LÝ DANH HIỆU
# =======================

@staff_required
def admin_badges(request):
    badges = Badge.objects.all().order_by('-id')
    return render(request, 'badge/admin_badges.html', {'badges': badges})


@staff_required
def add_badge(request):
    if request.method == 'POST':
        form = BadgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('badge:admin_badges')
    else:
        form = BadgeForm()
    return render(request, 'badge/badge_form.html', {
        'form': form,
        'title': 'Thêm danh hiệu mới'
    })


@staff_required
def edit_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    if request.method == 'POST':
        form = BadgeForm(request.POST, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('badge:admin_badges')
    else:
        form = BadgeForm(instance=badge)
    return render(request, 'badge/badge_form.html', {
        'form': form,
        'title': f'Chỉnh sửa: {badge.name}'
    })


@staff_required
def delete_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    badge.delete()
    return redirect('badge:admin_badges')


# =======================
# USER XEM & CHỌN DANH HIỆU
# =======================

@login_required
def user_badges(request):
    user = request.user
    badges = Badge.objects.all()
    progress_data = []
    achieved = []

    for b in badges:
        progress, _ = UserBadgeProgress.objects.get_or_create(user=user, badge=b)

        percent = 0
        if b.target > 0:
            percent = min(100, round((progress.progress / b.target) * 100))

        completed = progress.progress >= b.target

        item = {
            "id": b.id,
            "name": b.name,
            "icon": b.icon,
            "target": b.target,
            "progress": progress.progress,
            "percent": percent,
            "type": b.get_type_display(),
            "completed": completed,
            "color": b.color, # ✅ SỬA LỖI: Thêm dòng này
        }

        progress_data.append(item)

        if completed:
            achieved.append(item) # "achieved" giờ cũng sẽ có "color"

    profile, _ = UserProfile.objects.get_or_create(user=user)

    context = {
        "progress_data": progress_data,
        "achieved_badges": achieved,
        "achieved_badges_json": json.dumps(achieved, cls=DjangoJSONEncoder),
        "current_display_id": profile.display_badge.id if profile.display_badge else None,
    }
    return render(request, "badge/user_badges.html", context)


@login_required
def save_display_badge(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"})

    badge_id = request.POST.get("badge_id")
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if badge_id == "none":
        profile.display_badge = None
        profile.save(update_fields=['display_badge'])
        return JsonResponse({"status": "success"})

    try:
        badge = Badge.objects.get(id=badge_id)
    except Badge.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Danh hiệu không tồn tại"})

    progress = UserBadgeProgress.objects.filter(user=request.user, badge=badge).first()
    if not progress or progress.progress < badge.target:
        return JsonResponse({"status": "error", "message": "Chưa đạt danh hiệu này"})

    profile.display_badge = badge
    profile.save(update_fields=['display_badge'])

    return JsonResponse({"status": "success"})