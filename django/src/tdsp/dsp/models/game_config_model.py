from django.db import models
from django.utils import timezone


class ConfigModel(models.Model):
    IMPRESSIONS_CHOICES = [(1, '1'), (2, '2')]
    MODE_CHOICES = [('free', 'Free'), ('script', 'Script')]

    current = models.BooleanField(default=True)
    game_goal = models.CharField(max_length=20)
    impressions_total = models.IntegerField(blank=True, null=True)
    rounds_left = models.IntegerField(blank=True, null=True)
    auction_type = models.IntegerField(choices=IMPRESSIONS_CHOICES)
    mode = models.CharField(choices=MODE_CHOICES, max_length=10)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    impression_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    click_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    conversion_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    frequency_capping = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.mode} type config with id {self.id}"

    def save(self, *args, **kwargs):

        ConfigModel.objects.filter(current=True).update(current=False)
        super(ConfigModel, self).save(*args, **kwargs)
