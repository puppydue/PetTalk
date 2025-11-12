from django.db import models

class Badge(models.Model):
    # --- Các lựa chọn cho màu sắc và loại danh hiệu ---
    COLOR_CHOICES = [
        ("gold", "Vàng"),
        ("blue", "Xanh dương"),
        ("green", "Xanh lá"),
        ("red", "Đỏ"),
        ("cyan", "Xanh ngọc"),
        ("lime", "Xanh nhạt"),
    ]

    TYPE_CHOICES = [
        ("post", "Bài viết"),
        ("comment", "Bình luận"),
        ("reaction", "Tương tác"),
    ]

    # --- Trường dữ liệu chính ---
    name = models.CharField(max_length=100, verbose_name="Tên danh hiệu")
    description = models.TextField(verbose_name="Mô tả danh hiệu", blank=True)

    icon = models.CharField(
        max_length=20,
        blank=True,
        default="TROPHY",
        choices=[
            ("TROPHY", "TROPHY"), ("STAR", "STAR"), ("FIRE", "FIRE"), ("LIGHTNING", "LIGHTNING"),
            ("HEART", "HEART"), ("CHAT", "CHAT"), ("ROCKET", "ROCKET"), ("CROWN", "CROWN"),
            ("GIFT", "GIFT"), ("FLAG", "FLAG"), ("MEOW", "MEOW"), ("PAW", "PAW")
        ],
        verbose_name="Icon danh hiệu"
    )

    # --- Các trường mới để tính tiến trình ---
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default="post",
        verbose_name="Loại danh hiệu",
        help_text="Chọn loại hành động dùng để tính tiến trình (bài viết, bình luận, tương tác)"
    )
    target = models.PositiveIntegerField(
        default=1,
        verbose_name="Mục tiêu cần đạt",
        help_text="Số lượng cần đạt để hoàn thành danh hiệu"
    )

    color = models.CharField(
        max_length=20,
        choices=COLOR_CHOICES,
        default="blue",
        verbose_name="Màu hiển thị"
    )

    # --- Metadata ---
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    achieved_count = models.IntegerField(default=0, verbose_name="Số người đã đạt")

    def __str__(self):
        return self.name
