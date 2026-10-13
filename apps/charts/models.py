from django.db import models

# Create your models here.
class Chart(models.Model):
    id = models.AutoField(primary_key=True)
    door_location = models.JSONField(null=True, blank=True)
    house_facing = models.JSONField(null=True, blank=True)
    se = models.JSONField(null=True, blank=True)
    s = models.JSONField(null=True, blank=True)
    sw = models.JSONField(null=True, blank=True)
    e = models.JSONField(null=True, blank=True)
    w = models.JSONField(null=True, blank=True)
    ne = models.JSONField(null=True, blank=True)
    n = models.JSONField(null=True, blank=True)
    nw = models.JSONField(null=True, blank=True)
    center = models.JSONField(null=True, blank=True)
    sub_heaver = models.CharField(max_length=50, null=True, blank=True)
    sub_earthly = models.CharField(max_length=50, null=True, blank=True)
    aus_info = models.JSONField(null=True, blank=True)
    inaus_info = models.JSONField(null=True, blank=True)
    lead_stem = models.CharField(max_length=50, null=True, blank=True)
    house_stem_branch = models.CharField(max_length=50, null=True, blank=True)
    facing = models.CharField(max_length=50, null=True, blank=True)
    backing = models.CharField(max_length=50, null=True, blank=True)
    period_category = models.CharField(max_length=50, null=True, blank=True)
    preiod = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chart {self.id}"
    