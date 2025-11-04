from django.shortcuts import render, redirect, get_object_or_404
from .models import Badge
from .forms import BadgeForm

def admin_badges(request):
    badges = Badge.objects.all().order_by('-id')
    return render(request, 'badge/admin_badges.html', {'badges': badges})

def add_badge(request):
    if request.method == 'POST':
        form = BadgeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('badge:admin_badges')
    else:
        form = BadgeForm()
    return render(request, 'badge/badge_form.html', {'form': form, 'title': 'Thêm danh hiệu mới'})

def edit_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    if request.method == 'POST':
        form = BadgeForm(request.POST, instance=badge)
        if form.is_valid():
            form.save()
            return redirect('badge:admin_badges')
    else:
        form = BadgeForm(instance=badge)
    return render(request, 'badge/badge_form.html', {'form': form, 'title': f'Chỉnh sửa: {badge.name}'})

def delete_badge(request, badge_id):
    badge = get_object_or_404(Badge, id=badge_id)
    badge.delete()
    return redirect('badge:admin_badges')
