from .models import Event
from django.utils import timezone

def upcoming_events(request):
    """
    Trả về tối đa 5 sự kiện đã duyệt và chưa kết thúc để hiển thị ở right panel.
    """
    now = timezone.now()
    events = Event.objects.filter(status='approved', date__gte=now).order_by('date')[:5]
    return {'upcoming_events': events}
