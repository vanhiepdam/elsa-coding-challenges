from django.db import models

from core.utils.database import generate_snow_flake_id


class SnowFlakeIDModel(models.Model):
    id = models.BigIntegerField(primary_key=True, default=generate_snow_flake_id)

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
