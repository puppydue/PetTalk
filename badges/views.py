from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Badge, UserBadgeProgress

@login_required
def user_badges(request):
    badges = []
    all_badges = Badge.objects.all()

    for b in all_badges:
        progress_obj, _ = UserBadgeProgress.objects.get_or_create(
            user=request.user, badge=b
        )
        progress = progress_obj.progress
        remaining = max(b.target - progress, 0)
        percent = round(min(progress / b.target * 100, 100))

        badges.append({
            "name": b.name,
            "icon": b.icon,
            "target": b.target,
            "progress": progress,
            "percent": percent,
            "achievers": UserBadgeProgress.objects.filter(progress__gte=b.target).count(),
            "color": b.color,
            "is_completed": progress >= b.target,
            "remaining": remaining,           # ➜ thêm dòng này
        })

    ctx = {
        "badges": badges,
        "period_start": "1/1/2025",
        "period_end": "1/1/2026",
        "days_left": 71,
    }
    return render(request, "badges/user_badges.html", ctx)