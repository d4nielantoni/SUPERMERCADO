from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShoppingList(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Item(models.Model):
    shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField('Nome', max_length=200)
    quantity = models.IntegerField('Quantidade', null=True, blank=True)
    unit = models.CharField('Unidade', max_length=50, blank=True)
    purchased = models.BooleanField('Comprado', default=False)
    price = models.DecimalField('Preço', max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        if self.quantity and self.unit:
            return f"{self.name} ({self.quantity} {self.unit})"
        elif self.unit:
            return f"{self.name} ({self.unit})"
        return self.name
