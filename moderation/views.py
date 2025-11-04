from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from forum.models import ReportsPost, ReportsComment, Post, Comment
from Events.models import Event
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def is_moderator(user):
    return user.is_staff


@user_passes_test(is_moderator)
def moderation_reports(request):
    reports_post = ReportsPost.objects.all()
    reports_comment = ReportsComment.objects.all()
    context = {'reports_post': reports_post, 'reports_comment': reports_comment}
    return render(request, 'moderation/moderation_reports.html', context)


@user_passes_test(is_moderator)
def report_action(request, report_type, report_id):
    if request.method == 'POST':
        action = request.POST.get('action')

        # ✅ THÊM PHẦN XỬ LÝ THẬT Ở ĐÂY
        if report_type == 'post':
            report = get_object_or_404(ReportsPost, pk=report_id)
            content = report.post  # 🔹 lấy object bài viết thật
        else:
            report = get_object_or_404(ReportsComment, pk=report_id)
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
    pending_events = Event.objects.all().order_by('-created_at')
    context = {
        'pending_events': pending_events
    }
    return render(request, 'moderation/moderation_events.html', context)

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