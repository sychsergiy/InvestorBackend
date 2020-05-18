import enum

from django.db import models
from django.contrib.auth import get_user_model

from apps.asset.models import Asset


class Purchase(models.Model):
    class Types(enum.Enum):
        BUY = "Buy"
        SELL = "Sell"

    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT)
    asset_amount = models.FloatField()
    absolute_amount = models.FloatField()
    type = models.CharField(
        max_length=68, choices=[(tag.name, tag.value) for tag in Types]
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} {self.asset}"
