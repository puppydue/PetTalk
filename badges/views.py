# badges/views.py
from django.shortcuts import render
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from badge.models import Badge
from .models import UserBadgeProgress
from profiles.models import UserProfile

@login_required
def user_badges(request):
    user = request.user
    badges = Badge.objects.all()
    progress_data = []
    achieved_badges = []

    for b in badges:
        progress, _ = UserBadgeProgress.objects.get_or_create(user=user, badge=b)

        total = b.target
        value = progress.progress
        percent = min(100, round((value / total) * 100)) if total > 0 else 0
        completed = value >= total

        item = {
            "name": b.name,
            "target": total,
            "progress": value,
            "percent": percent,
            "type": b.get_type_display(),
            "completed": completed,
            "color": b.color,
        }
        progress_data.append(item)

        if completed:
            achieved_badges.append(item)

    profile, _ = UserProfile.objects.get_or_create(user=user)

    context = {
        "progress_data": progress_data,
        "achieved_badges": achieved_badges,
        "achieved_badges_json": json.dumps(achieved_badges, cls=DjangoJSONEncoder),
    }
    return render(request, "badges/user_badges.html", context)


# API: Lưu badge được chọn
@login_required
def save_display_badge(request):
    if request.method == "POST":
        badge_name = request.POST.get("badge_name")

        print(f"[SAVE BADGE] User: {request.user}, badge: {badge_name}")  # LOG
        profile, _ = UserProfile.objects.get_or_create(user=request.user)

        if badge_name == "none":
            profile.display_badge = None
        else:
            try:
                badge = Badge.objects.get(name=badge_name)
                # Kiểm tra xem user có thực sự đạt badge này không
                progress = UserBadgeProgress.objects.get(user=request.user, badge=badge)
                if progress.progress >= badge.target:
                    profile.display_badge = badge
                else:
                    return JsonResponse({"status": "error", "message": "Chưa đạt danh hiệu này"})
            except Badge.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Danh hiệu không tồn tại"})

        profile.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "message": "Invalid request"})