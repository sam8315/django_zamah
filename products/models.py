from django.db import models
from django.shortcuts import reverse


class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})
