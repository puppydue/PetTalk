from django.db.models.signals import post_save
from django.dispatch import receiver
from forum.models import Post, Comment
from django.contrib.auth.models import User
from moderation.models import ForbiddenKeyword
from forum.models import ReportsPost, ReportsComment

@receiver(post_save, sender=Post)
def auto_report_post(sender, instance, created, **kwargs):
    if not created:
        return

    keywords = ForbiddenKeyword.objects.all()
    content = (instance.title + " " + instance.content).lower()

    for kw in keywords:
        if kw.word.lower() in content:
            admin_user = User.objects.filter(is_superuser=True).first()

            ReportsPost.objects.create(
                post=instance,
                reporter=admin_user,
                reason=f"Tự động phát hiện từ khóa vi phạm: '{kw.word}'",
                status="pending"
            )
            break  # tạo 1 báo cáo là đủ


@receiver(post_save, sender=Comment)
def auto_report_comment(sender, instance, created, **kwargs):
    if not created:
        return

    keywords = ForbiddenKeyword.objects.all()
    content = instance.content.lower()

    for kw in keywords:
        if kw.word.lower() in content:
            admin_user = User.objects.filter(is_superuser=True).first()

            ReportsComment.objects.create(
                comment=instance,
                username=admin_user,
                reason=f"Tự động phát hiện từ khóa vi phạm: '{kw.word}'",
                status="pending"
            )
            break
