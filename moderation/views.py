from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from forum.models import Reports_post, Reports_comment, Post, Comment
from Events.models import Event_Registration, Event
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def is_moderator(user):
    return user.is_staff


@user_passes_test(is_moderator)
def moderation_reports(request):
    reports_post = Reports_post.objects.all()
    reports_comment = Reports_comment.objects.all()
    context = {'reports_post': reports_post, 'reports_comment': reports_comment}
    return render(request, 'moderation/moderation_reports.html', context)


@user_passes_test(is_moderator)
def report_detail(request, report_type, report_id):
    if report_type == 'post':
        report = get_object_or_404(Reports_post, pk=report_id)
    else:
        report = get_object_or_404(Reports_comment, pk=report_id)
    data = {
        'type': report_type,
        'user': report.username.username,
        'reason': report.reason,
        'details': report.details,
        'status': report.status,
        'created_at': report.created_at.strftime("%d/%m/%Y %H:%M")
    }
    return JsonResponse(data)


@user_passes_test(is_moderator)
def report_action(request, report_type, report_id):
    if request.method == 'POST':
        action = request.POST.get('action')

        # ✅ THÊM PHẦN XỬ LÝ THẬT Ở ĐÂY
        if report_type == 'post':
            report = get_object_or_404(Reports_post, pk=report_id)
            content = report.post  # 🔹 lấy object bài viết thật
        else:
            report = get_object_or_404(Reports_comment, pk=report_id)
            content = report.comment  # 🔹 lấy object bình luận thật

        if action == 'delete':
            content.delete()  # 🔥 xóa thật bài viết hoặc bình luận
            report.status = 'deleted'
        elif action == 'dismiss':
            report.status = 'dismissed'

        report.save()
        return JsonResponse({'success': True, 'new_status': report.status})

    return JsonResponse({'success': False})


# ==========================================================
# ✅ THÊM PHẦN LIÊN KẾT DUYỆT SỰ KIỆN
# ==========================================================

@user_passes_test(is_moderator)
def moderation_events(request):
    # Lấy các sự kiện chờ duyệt
    pending_events = Event.objects.filter(status='pending').select_related('creator').order_by('-created_at')

    context = {
        'pending_events': pending_events
    }
    return render(request, 'moderation/moderation_events.html', context)


@user_passes_test(is_moderator)
def event_detail(request, regis_id):
    regis = get_object_or_404(Event_Registration, pk=regis_id)
    data = {
        'user': regis.username.username,
        'event': regis.event.title,
        'registered_at': regis.requested_at.strftime("%d/%m/%Y %H:%M"),
        'status': regis.status if hasattr(regis, 'status') else 'pending'
    }
    return JsonResponse(data)


@user_passes_test(is_moderator)
def event_action(request, regis_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        regis = get_object_or_404(Event_Registration, pk=regis_id)

        # ✅ thêm phần cập nhật trạng thái đăng ký thật
        if not hasattr(regis, 'status'):
            regis.status = 'pending'

        if action == 'approve':
            regis.status = 'approved'
        elif action == 'reject':
            regis.status = 'rejected'

        regis.save()
        return JsonResponse({'success': True, 'new_status': regis.status})

    return JsonResponse({'success': False})

@user_passes_test(is_moderator)
def event_action(request, event_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        event = get_object_or_404(Event, pk=event_id)
        if action == 'approve':
            event.status = 'approved'
        elif action == 'reject':
            event.status = 'rejected'
        event.save()
        return JsonResponse({'success': True, 'new_status': event.status})
    return JsonResponse({'success': False})


@user_passes_test(is_moderator)
def update_event_status(request, event_id):
    """
    API cho moderator phê duyệt hoặc từ chối sự kiện
    """
    if request.method == 'POST':
        try:
            event = Event.objects.get(id=event_id)
            action = request.POST.get('action')

            if action == 'approve':
                event.status = 'approved'
            elif action == 'reject':
                event.status = 'rejected'
            else:
                return JsonResponse({'success': False, 'error': 'Invalid action'})

            event.save()
            return JsonResponse({'success': True, 'new_status': event.status})
        except Event.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event not found'})
    return JsonResponse({'success': False, 'error': 'Invalid method'})