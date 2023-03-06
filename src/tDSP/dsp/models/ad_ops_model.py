from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from ...tools.image_proc import handle_uploaded_file


class AdOpsModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=handle_uploaded_file, blank=True, null=True)
    registered_at = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'AdOp'

    def __str__(self):
        return self.user.username

