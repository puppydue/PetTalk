# context_processors.py

# ✅ SỬA LỖI: Dùng import tuyệt đối (absolute import)
# an toàn hơn là "from .models import Post"
from forum.models import Post
from django.db.models import Count


def topic_choices(request):
    """
    Trả danh sách 4 CHỦ ĐỀ NỔI BẬT NHẤT (nhiều bài post nhất)
    ra mọi template.
    """

    # 1. Lấy danh sách (value, label) gốc
    # Ví dụ: {'dinhduong': 'Dinh dưỡng & Thức ăn', 'huanluyen': 'Huấn luyện & Hành vi', ...}
    topic_labels = dict(Post.TOPIC_CHOICES)

    # 2. Query Database:
    # - Group by 'topic'
    # - Đếm số bài trong mỗi group (post_count)
    # - Sắp xếp từ cao xuống thấp
    # - Lấy 4 chủ đề đầu tiên
    top_topics_data = Post.objects.values('topic') \
        .annotate(post_count=Count('post_id')) \
        .order_by('-post_count')[:4]

    # 3. Tạo lại danh sách (value, label) mới
    # top_topics_data bây giờ là:
    # [ {'topic': 'hinh_anh', 'post_count': 50}, {'topic': 'dinhduong', 'post_count': 32}, ... ]

    top_topic_choices = []
    for item in top_topics_data:
        value = item['topic']
        # Lấy label (tên đầy đủ) từ dict ở bước 1
        label = topic_labels.get(value, value.capitalize())
        top_topic_choices.append((value, label))

    # 4. Trả về biến 'topic_choices' (base.html sẽ tự động dùng biến này)
    return {'topic_choices': top_topic_choices}