# badges/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from forum.models import Post, Comment, Reaction
from badge.models import Badge  # Import Badge từ app badge
from .models import UserBadgeProgress
from django.contrib.auth.models import User


@receiver(post_save, sender=Badge)  # 👈 Thêm signal này cho badge mới
def handle_new_badge(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            # Tạo progress với counts hiện tại của user
            post_count = Post.objects.filter(username=user).count()
            comment_count = Comment.objects.filter(username=user).count()
            reaction_count = Reaction.objects.filter(username=user).count()

            progress = UserBadgeProgress.objects.create(
                user=user,
                badge=instance,
                post_count=post_count,
                comment_count=comment_count,
                reaction_count=reaction_count,
            )
            progress.update_progress()  # Tính progress dựa type


def _get_or_create_progress(user):
    """Tạo đủ các record UserBadgeProgress cho user tương ứng với mỗi Badge."""
    for badge in Badge.objects.all():
        UserBadgeProgress.objects.get_or_create(user=user, badge=badge)


def _update_progress_counts(user):
    """Cập nhật tổng số post/comment/reaction của user."""
    post_count = Post.objects.filter(username=user).count()
    comment_count = Comment.objects.filter(username=user).count()
    reaction_count = Reaction.objects.filter(username=user).count()

    # Duyệt tất cả tiến trình của user
    for progress in UserBadgeProgress.objects.filter(user=user):
        # Ghi nhận số đếm mới
        progress.post_count = post_count
        progress.comment_count = comment_count
        progress.reaction_count = reaction_count

        # Tính tổng progress (tùy vào loại badge)
        progress.update_progress()  # 👈 Gọi method để tính và save

        # 👈 Thêm: Update achieved_count cho badge
        badge = progress.badge
        badge.achieved_count = UserBadgeProgress.objects.filter(
            badge=badge, progress__gte=badge.target
        ).count()
        badge.save(update_fields=['achieved_count'])


@receiver([post_save, post_delete], sender=Post)
def update_post_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress(user)
    _update_progress_counts(user)


@receiver([post_save, post_delete], sender=Comment)
def update_comment_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress(user)
    _update_progress_counts(user)


@receiver([post_save, post_delete], sender=Reaction)
def update_reaction_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress(user)
    _update_progress_counts(user)