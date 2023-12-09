from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    alcohol_type = models.CharField(max_length=50, default='Без регистрации')
    quantity = models.PositiveIntegerField(default=0)

    def decrease_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)