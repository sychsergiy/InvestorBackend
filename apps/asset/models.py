import enum
from django.db import models


class Asset(models.Model):
    class Categories(enum.Enum):
        CRYPTO_CURRENCY = "CryptoCurrency"
        PRECIOUS_METAL = "PreciousMetal"
        STOCK = "Stock"

    name = models.CharField(max_length=128, unique=True)
    category = models.CharField(
        max_length=64,
        choices=[(tag.name, tag.value) for tag in Categories],
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
