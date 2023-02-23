from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.id}: {self.name}"


class Offer(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='offers')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.price} - {self.items_in_stock} ({self.product})"
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title