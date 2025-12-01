from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseBadRequest
from forum.models import Post, Comment, ReportsPost, ReportsComment
from django.contrib.auth.decorators import user_passes_test, login_required
from Events.models import Event
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Count
from django.utils.html import strip_tags
from django.utils import timezone
from datetime import timedelta
from .models import ForbiddenKeyword
from django.contrib import messages

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
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    action = request.POST.get('action')
    if action not in ('approve', 'reject'):
        return JsonResponse({'success': False, 'error': 'Invalid action'})

    if rtype not in ('post', 'comment'):
        return JsonResponse({'success': False, 'error': 'Invalid report type'})

    try:
        # ===============================
        # XỬ LÝ BÁO CÁO BÀI VIẾT
        # ===============================
        if rtype == 'post':
            report = ReportsPost.objects.select_related('post').get(pk=rid)

            if action == 'approve':
                new_status = "approved"

                if report.post:     # nếu bài viết chưa bị xóa
                    report.post.delete()
                    report.post = None

            else:
                new_status = "rejected"

            report.status = new_status
            report.save()

        # ===============================
        # XỬ LÝ BÁO CÁO BÌNH LUẬN
        # ===============================
        else:
            report = ReportsComment.objects.select_related('comment').get(pk=rid)

            if action == 'approve':
                new_status = "approved"

                if report.comment:
                    report.comment.delete()
                    report.comment = None
            else:
                new_status = "rejected"

            report.status = new_status
            report.save()

        # 🔥 Không trả về related ID nữa
        return JsonResponse({
            "success": True,
            "new_status": new_status
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


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

@login_required
@user_passes_test(is_moderator)
def moderation_stats(request):

    range_filter = request.GET.get("range", "today")
    now = timezone.now()

    # --- Bộ lọc thời gian ---
    if range_filter == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    elif range_filter == "yesterday":
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0)
        end = (now - timedelta(days=1)).replace(hour=23, minute=59, second=59)

    elif range_filter == "week":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0)

    elif range_filter == "month":
        start = now.replace(day=1, hour=0, minute=0, second=0)

    else:  # all time
        start = None

    # ------ Lấy dữ liệu ------
    rp_post = ReportsPost.objects.all()
    rp_cmt = ReportsComment.objects.all()

    if start:
        rp_post = rp_post.filter(created_at__gte=start)
        rp_cmt = rp_cmt.filter(created_at__gte=start)

    # --- Tổng số ---
    total_reports = rp_post.count() + rp_cmt.count()
    total_post_reports = rp_post.count()
    total_comment_reports = rp_cmt.count()

    # --- Tình trạng xử lý ---
    pending = rp_post.filter(status="pending").count() + rp_cmt.filter(status="pending").count()
    approved = rp_post.filter(status="approved").count() + rp_cmt.filter(status="approved").count()
    rejected = rp_post.filter(status="rejected").count() + rp_cmt.filter(status="rejected").count()

    resolved = approved + rejected
    handled_rate = 0 if total_reports == 0 else round((resolved / total_reports) * 100)

    # --- TOP bài viết pending ---
    top_post = (
        rp_post.filter(status="pending", post__isnull=False)
        .values("post_id", "post__title")
        .annotate(count=Count("post_id"))
        .order_by("-count")[:5]
    )

    # --- TOP bình luận pending ---
    top_comment = (
        rp_cmt.filter(status="pending", comment__isnull=False)
        .values("comment_id", "comment__content")
        .annotate(count=Count("comment_id"))
        .order_by("-count")[:5]
    )

    # ------ Trả về template ------
    context = {
        "total_reports": total_reports,
        "total_post": total_post_reports,
        "total_comment": total_comment_reports,

        "handled_rate": handled_rate,
        "pending": pending,
        "approved": approved,
        "rejected": rejected,

        "top_post": top_post,
        "top_comment": top_comment,

        "range_filter": range_filter,
    }

    return render(request, "moderation/moderation_stats.html", context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def moderation_keywords(request):
    keywords = ForbiddenKeyword.objects.all().order_by('-id')

    if request.method == "POST":
        new_kw = request.POST.get('keyword').strip()

        if ForbiddenKeyword.objects.filter(word__iexact=new_kw).exists():
            messages.error(request, "Từ khóa này đã tồn tại.")
        else:
            ForbiddenKeyword.objects.create(word=new_kw)
            messages.success(request, f"Đã thêm từ khóa '{new_kw}'.")

        return redirect("moderation_keywords")

    return render(request, "moderation/moderation_keywords.html", {
        "keywords": keywords
    })

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_keyword(request, pk):
    kw = get_object_or_404(ForbiddenKeyword, pk=pk)
    kw.delete()
    messages.success(request, "Đã xoá từ khóa cấm.")
    return redirect("moderation_keywords")