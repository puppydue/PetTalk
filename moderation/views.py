from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from forum.models import Post, Comment, ReportsPost, ReportsComment
from django.contrib.auth.decorators import user_passes_test, login_required
from Events.models import Event
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from django.utils.html import strip_tags



def is_moderator(user):
    # Tuỳ team: có thể check group 'moderator' hay permission
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_moderator)
def moderation_reports(request):
    """Trang danh sách báo cáo + bộ lọc"""
    type_filter = request.GET.get('type', 'all')        # all | post | comment
    status_filter = request.GET.get('status', 'all')    # all | pending | approved | rejected

    items = []

    # Reports Post
    if type_filter in ('all', 'post'):
        qs = ReportsPost.objects.select_related('post', 'reporter').order_by('-created_at')
        if status_filter != 'all':
            qs = qs.filter(status=status_filter)
        for r in qs:
            target_title = getattr(r.post, 'title', '(đã xóa)') if r.post else '(đã xóa)'
            target_preview = strip_tags(getattr(r.post, 'content', '')[:160]) if r.post else ''
            items.append({
                'rtype': 'post',
                'rid': r.pk,
                'reporter': r.reporter.username,
                'reason': r.reason,
                'details': r.details or '',
                'created_at': r.created_at,
                'status': r.status,
                'target_title': target_title,
                'target_preview': target_preview,
            })

    # Reports Comment
    if type_filter in ('all', 'comment'):
        qs = ReportsComment.objects.select_related('comment', 'username').order_by('-created_at')
        if status_filter != 'all':
            qs = qs.filter(status=status_filter)
        for r in qs:
            target_title = f"Bình luận #{getattr(r.comment, 'pk', '')}" if r.comment else '(đã xóa)'
            target_preview = strip_tags(getattr(r.comment, 'content', '')[:160]) if r.comment else ''
            items.append({
                'rtype': 'comment',
                'rid': r.pk,
                'reporter': r.username.username,
                'reason': r.reason,
                'details': r.details or '',
                'created_at': r.created_at,
                'status': r.status,
                'target_title': target_title,
                'target_preview': target_preview,
            })

    # Sắp xếp tất cả báo cáo mới nhất trước
    items.sort(key=lambda x: x['created_at'], reverse=True)

    # Bộ lọc (đưa ra context để tránh lỗi template)
    type_options = [
        ('Tất cả', 'all'),
        ('Bài viết', 'post'),
        ('Bình luận', 'comment'),
    ]
    status_options = [
        ('Tất cả', 'all'),
        ('Pending', 'pending'),
        ('Approved', 'approved'),
        ('Rejected', 'rejected'),
    ]

    context = {
        'reports': items,
        'type_filter': type_filter,
        'status_filter': status_filter,
        'type_options': type_options,
        'status_options': status_options,
    }
    return render(request, 'moderation/moderation_reports.html', context)


@login_required
@user_passes_test(is_moderator)
def update_report_status(request, rtype, rid):
    """AJAX: approve/reject report. Approve => xóa Post/Comment; giữ lại report với status='approved'"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    action = request.POST.get('action')
    if rtype not in ('post', 'comment') or action not in ('approve', 'reject'):
        return JsonResponse({'success': False, 'error': 'Invalid params'})

    try:
        if rtype == 'post':
            report = ReportsPost.objects.select_related('post').get(pk=rid)
            # Nếu approve -> xóa bài
            if action == 'approve' and report.status != 'approved':
                if report.post:
                    report.post.delete()
                    report.post = None  # <--- ✅ THÊM DÒNG NÀY
                report.status = 'approved'
            elif action == 'reject':
                report.status = 'rejected'
            report.save()


        else:  # comment
            report = ReportsComment.objects.select_related('comment').get(pk=rid)
            # Nếu approve -> xóa comment
            if action == 'approve' and report.status != 'approved':
                if report.comment:
                    report.comment.delete()
                    report.comment = None  # <--- ✅ THÊM DÒNG NÀY
                report.status = 'approved'
            elif action == 'reject':
                report.status = 'rejected'
            report.save()
        return JsonResponse({'success': True, 'new_status': report.status})

    except (ReportsPost.DoesNotExist, ReportsComment.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Report not found'})


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