# analytics/models.py
from django.db import models
from django.utils import timezone


class PageView(models.Model):
    url = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.url} - {self.timestamp}"


class DailyPageViewCount(models.Model):
    url = models.CharField(max_length=255)
    date = models.DateField()
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("url", "date")

    def __str__(self):
        return f"{self.url} - {self.date}: {self.count} views"


class UniqueVisitor(models.Model):
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    first_visit = models.DateTimeField(default=timezone.now)
    last_visit = models.DateTimeField(default=timezone.now)
    visit_count = models.PositiveIntegerField(default=1)
    is_bot = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if "bot" in self.user_agent.lower():
            self.is_bot = True
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("ip_address", "user_agent")

    def most_common_url(self):
        """
        Returns the URL of the most recent PageView for this visitor,
        or None if no page views are found.
        """
        # Get the most recent PageView object for this visitor
        latest_page_view = (
            PageView.objects.filter(ip_address=self.ip_address)
            .order_by("-timestamp")
            .first()
        )

        # Check if a page view was actually found before accessing its url
        if latest_page_view:
            return latest_page_view.url

        # Return None or a default value if no page views exist for visitor
        return None

    def __str__(self):
        return f"{self.ip_address} - Visits: {self.visit_count}"
