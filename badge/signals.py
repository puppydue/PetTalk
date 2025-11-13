# badge/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User

from forum.models import Post, Comment, Reaction
from .models import Badge, UserBadgeProgress


@receiver(post_save, sender=Badge)
def handle_new_badge(sender, instance, created, **kwargs):
    """
    Khi tạo 1 Badge mới, tự tạo UserBadgeProgress tương ứng cho tất cả user hiện tại.
    """
    if not created:
        return

    for user in User.objects.all():
        post_count = Post.objects.filter(username=user).count()
        comment_count = Comment.objects.filter(username=user).count()
        reaction_count = Reaction.objects.filter(username=user).count()

        progress, _ = UserBadgeProgress.objects.get_or_create(
            user=user,
            badge=instance,
            defaults={
                "post_count": post_count,
                "comment_count": comment_count,
                "reaction_count": reaction_count,
            }
        )
        progress.update_progress(save=True)


def _get_or_create_progress_for_user(user):
    """
    Đảm bảo user có đủ record UserBadgeProgress cho tất cả Badge hiện có.
    """
    for badge in Badge.objects.all():
        UserBadgeProgress.objects.get_or_create(user=user, badge=badge)


def _recalculate_user_progress(user):
    """
    Cập nhật lại post_count, comment_count, reaction_count cho user,
    sau đó tính lại progress + cập nhật achieved_count cho từng badge.
    """
    post_count = Post.objects.filter(username=user).count()
    comment_count = Comment.objects.filter(username=user).count()
    reaction_count = Reaction.objects.filter(username=user).count()

    progresses = UserBadgeProgress.objects.filter(user=user, badge__isnull=False)

    for progress in progresses:
        progress.post_count = post_count
        progress.comment_count = comment_count
        progress.reaction_count = reaction_count
        progress.update_progress(save=True)

        badge = progress.badge
        if badge:
            badge.achieved_count = UserBadgeProgress.objects.filter(
                badge=badge,
                progress__gte=badge.target
            ).count()
            badge.save(update_fields=['achieved_count'])


@receiver([post_save, post_delete], sender=Post)
def update_post_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress_for_user(user)
    _recalculate_user_progress(user)


@receiver([post_save, post_delete], sender=Comment)
def update_comment_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress_for_user(user)
    _recalculate_user_progress(user)


@receiver([post_save, post_delete], sender=Reaction)
def update_reaction_count(sender, instance, **kwargs):
    user = instance.username
    _get_or_create_progress_for_user(user)
    _recalculate_user_progress(user)
