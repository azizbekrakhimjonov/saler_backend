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


from django.core.management.base import BaseCommand
from random import choices
from string import ascii_uppercase, digits

class Command(BaseCommand):
    help = "Generate and populate promocodes"

    def handle(self, *args, **kwargs):
        categories = {
            'category1': 5,
            'category2': 10,
            'category3': 15,
            # Add more categories as needed
        }

        for category, point in categories.items():
            for _ in range(100):  # Generate 100 promocodes per category
                code = ''.join(choices(ascii_uppercase + digits, k=6))
                Promocode.objects.get_or_create(
                    code=code,
                    defaults={'category': category, 'point': point}
                )

        self.stdout.write(self.style.SUCCESS("Promocodes generated successfully!"))

