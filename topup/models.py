from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=100)
    game_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TopUpProduct(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_game_currency = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.game.name})"

class TopUpOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    user_email = models.EmailField()
    product = models.ForeignKey(TopUpProduct, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_email} - {self.product.name} - {self.status}"

