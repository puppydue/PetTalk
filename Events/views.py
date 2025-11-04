from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Event
from .forms import EventForm


# 1️⃣ Tạo sự kiện
@login_required
def tao_su_kien(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            # Ràng buộc: không cho ngày kết thúc < ngày bắt đầu
            if event.end_date and event.end_date < event.date:
                messages.error(request, "⛔ Thời gian kết thúc không được trước thời gian bắt đầu.")
                return render(request, 'events/tao_su_kien.html', {'form': form})

            event.creator = request.user
            event.status = 'pending'
            event.save()
            messages.success(request, "🎉 Sự kiện đã được gửi chờ phê duyệt.")
            return redirect('danh_sach_su_kien')
    else:
        form = EventForm()

    return render(request, 'events/tao_su_kien.html', {'form': form})


# 2️⃣ Chỉnh sửa sự kiện
@login_required
def chinh_sua_su_kien(request, event_id):
    event = get_object_or_404(Event, id=event_id, creator=request.user)

    # ⛔ Không cho chỉnh sửa nếu sự kiện đã kết thúc
    if event.is_past():
        messages.error(request, f"⛔ Sự kiện '{event.title}' đã kết thúc, không thể chỉnh sửa.")
        return redirect('danh_sach_su_kien')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            updated = form.save(commit=False)
            # Ràng buộc: end_date không nhỏ hơn start_date
            if updated.end_date and updated.end_date < updated.date:
                messages.error(request, "⛔ Thời gian kết thúc không được trước thời gian bắt đầu.")
                return render(request, 'events/chinh_sua_su_kien.html', {'form': form})
            updated.save()
            messages.success(request, f"✅ Sự kiện '{event.title}' đã được cập nhật thành công!")
            return redirect('danh_sach_su_kien')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/chinh_sua_su_kien.html', {'form': form})


# 3️⃣ Xoá sự kiện
@login_required
def xoa_su_kien(request, event_id):
    event = get_object_or_404(Event, id=event_id, creator=request.user)
    if request.method == 'POST':
        event.delete()
        messages.warning(request, "🗑️ Sự kiện đã bị xoá.")
        return redirect('danh_sach_su_kien')
    return render(request, 'events/xoa_su_kien.html', {'event': event})


# 4️⃣ Phê duyệt sự kiện (Moderator)
@user_passes_test(lambda u: u.is_staff)
def phe_duyet_su_kien(request):
    if request.method == 'POST':
        if 'approve' in request.POST:
            event = Event.objects.get(id=request.POST['approve'])
            event.status = 'approved'
            event.save()
            messages.success(request, f"✅ Đã phê duyệt sự kiện: {event.title}")
        elif 'reject' in request.POST:
            event = Event.objects.get(id=request.POST['reject'])
            event.status = 'rejected'
            event.save()
            messages.error(request, f"❌ Đã từ chối sự kiện: {event.title}")

    pending_events = Event.objects.filter(status='pending')
    return render(request, 'events/phe_duyet_su_kien.html', {'pending_events': pending_events})


# 5️⃣ Đăng ký tham gia sự kiện
@login_required
def dang_ky_tham_gia(request, event_id):
    event = get_object_or_404(Event, id=event_id, status='approved')

    # ⛔ Không cho đăng ký nếu sự kiện đã kết thúc
    if event.is_past():
        messages.warning(request, f"⏰ Sự kiện '{event.title}' đã kết thúc, bạn không thể đăng ký nữa.")
        return redirect('danh_sach_su_kien')

    if request.method == 'POST':
        if not event.participants.filter(id=request.user.id).exists():
            event.participants.add(request.user)
            messages.success(request, f"🐾 Bạn đã đăng ký tham gia sự kiện '{event.title}' thành công!")
        else:
            messages.warning(request, f"⚠️ Bạn đã đăng ký sự kiện '{event.title}' trước đó rồi.")
        return redirect('danh_sach_su_kien')

    return render(request, 'events/dang_ky_tham_gia.html', {'event': event})


# 6️⃣ Huỷ đăng ký tham gia
@login_required
def huy_dang_ky_tham_gia(request, event_id):
    event = get_object_or_404(Event, id=event_id, status='approved')

    # ⛔ Không cho huỷ đăng ký nếu sự kiện đã kết thúc
    if event.is_past():
        messages.error(request, f"⏰ Sự kiện '{event.title}' đã kết thúc, không thể huỷ đăng ký.")
        return redirect('danh_sach_su_kien')

    if request.method == 'POST':
        if event.participants.filter(id=request.user.id).exists():
            event.participants.remove(request.user)
            messages.warning(request, f"❌ Bạn đã huỷ đăng ký tham gia sự kiện '{event.title}' thành công!")
        else:
            messages.error(request, f"⚠️ Bạn chưa đăng ký sự kiện '{event.title}' nên không thể huỷ.")
        return redirect('danh_sach_su_kien')

    return render(request, 'events/huy_dang_ky_tham_gia.html', {'event': event})


# 7️⃣ Danh sách sự kiện
@login_required
def danh_sach_su_kien(request):
    # 🧍‍♂️ Sự kiện của tôi (gồm pending / approved / rejected)
    su_kien_cua_toi = Event.objects.filter(creator=request.user).order_by('-date')
    # 🌍 Danh sách sự kiện được phê duyệt
    danh_sach_su_kien = Event.objects.filter(status='approved').order_by('-date')

    context = {
        'su_kien_cua_toi': su_kien_cua_toi,
        'danh_sach_su_kien': danh_sach_su_kien,
        'now': timezone.now(),  # để so sánh trong template
    }
    return render(request, 'events/danh_sach_su_kien.html', context)


# 8️⃣ Danh sách người đăng ký
@login_required
def danh_sach_nguoi_dang_ky(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = event.participants.all() if hasattr(event, 'participants') else []
    return render(request, 'events/danh_sach_nguoi_dang_ky.html', {
        'event': event,
        'participants': participants
    })
