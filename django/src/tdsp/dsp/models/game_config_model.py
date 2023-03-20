from django.db import models
from django.utils import timezone


class ConfigModel(models.Model):
    """
    Represents a configuration model in the system.

    Attributes:
        IMPRESSIONS_CHOICES (list of tuples): The available choices for the auction type.
        MODE_CHOICES (list of tuples): The available choices for the configuration mode.
        current (bool): Indicates if the configuration is the current active one.
        game_goal (str): The goal of the game.
        impressions_total (int): The total impressions of the configuration.
        rounds_left (int): The remaining rounds of the configuration.
        auction_type (int): The type of auction.
        mode (str): The mode of the configuration.
        budget (Decimal): The budget of the configuration.
        impression_revenue (Decimal): The revenue generated from impressions.
        click_revenue (Decimal): The revenue generated from clicks.
        conversion_revenue (Decimal): The revenue generated from conversions.
        frequency_capping (int): The frequency capping of the configuration.
        created_at (datetime): The datetime the configuration was created.

    Methods:
        __str__(): Returns a string representation of the ConfigModel instance.
        save(*args, **kwargs): Saves the ConfigModel instance to the database and updates the current active configuration.
    """

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
        """
        Returns a string representation of the ConfigModel instance.

        Returns:
            str: A string representing the ConfigModel instance.
        """
        return f"{self.mode} type config with id {self.id}"

    def save(self, *args, **kwargs):
        """
        Saves the ConfigModel instance to the database and updates the current active configuration.

        Args:
            *args: Additional positional arguments to be passed to the parent method.
            **kwargs: Additional keyword arguments to be passed to the parent method.
        """
        ConfigModel.objects.filter(current=True).update(current=False)
        super(ConfigModel, self).save(*args, **kwargs)
