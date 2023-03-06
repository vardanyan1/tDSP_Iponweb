from django.db import models


class ConfigModel(models.Model):
    IMPRESSIONS_CHOICES = [(1, '1'), (2, '2')]
    MODE_CHOICES = [('free', 'Free'), ('script', 'Script')]

    current = models.BooleanField(default=True)
    impressions_total = models.IntegerField(blank=True, null=True)
    auction_type = models.IntegerField(choices=IMPRESSIONS_CHOICES)
    mode = models.CharField(choices=MODE_CHOICES, max_length=10)
    budget = models.IntegerField()
    impression_revenue = models.IntegerField()
    click_revenue = models.IntegerField()
    conversion_revenue = models.IntegerField()
    frequency_capping = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.mode} type config with id {self.id}"

    def save(self, *args, **kwargs):

        ConfigModel.objects.filter(current=True).update(current=False)
        super(ConfigModel, self).save(*args, **kwargs)
