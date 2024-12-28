from django.db import models


class Promocode(models.Model):
    code = models.CharField(max_length=6, unique=True, verbose_name="Promo Code")
    category = models.CharField(max_length=50, verbose_name="Category")
    point = models.IntegerField(verbose_name="Points")
    used_by = models.CharField(max_length=255, null=True, blank=True, verbose_name="Used By")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Promocode"
        verbose_name_plural = "Promocodes"


class User(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    is_registered = models.BooleanField(default=False)
    points = models.IntegerField(default=5)  # Ro'yxatdan o'tganida 5 ball beriladi

    def __str__(self):
        return self.fullname
