from django.db import models

class Product(models.Model):

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sizes = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('F', 'Free'),
    )
    size = models.CharField(choices=sizes, max_length=1)
    stock_quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.pk:
            self.stock_quantity = 0
        super().save(*args, **kwargs)


class Inbound(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product} - {self.quantity} 개 입고 ({self.date})'

class Outbound(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.product} - {self.quantity} 개 출고 ({self.date})'

class Inventory(models.Model):

    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product} - {self.quantity}'