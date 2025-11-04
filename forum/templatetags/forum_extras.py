# tạo thư mục templatetags bên trong app forum (nếu chưa có),
# nhớ có file __init__.py rỗng trong thư mục này
from django import template

register = template.Library()

@register.simple_tag
def reaction_of(post, user):
    """Trả về 'upvote' | 'downvote' | '' cho user hiện tại trên post."""
    if not getattr(user, "is_authenticated", False):
        return ''
    r = post.reactions.filter(username=user).first()
    return r.type if r else ''
