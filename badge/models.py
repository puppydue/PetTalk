from django.db import models

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    achieved_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
