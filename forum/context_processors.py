from .models import Post

def topic_choices(request):
    """
    Trả danh sách chủ đề (topic) ra mọi template.
    """
    return {'topic_choices': Post.TOPIC_CHOICES}