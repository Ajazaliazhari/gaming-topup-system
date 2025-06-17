from django.db import models


from django.db import models

class Game(models.Model):
    """
    Represents a game in the system.
    """
    name = models.CharField(max_length=255, unique=True, help_text="The common name of the game (e.g., 'PUBG Mobile').")
    game_id = models.CharField(max_length=100, unique=True, help_text="A unique identifier for the game (e.g., 'pubg123').")
    is_active = models.BooleanField(default=True, help_text="Indicates if the game is currently active for top-ups.")

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.game_id})"

class TopUpProduct(models.Model):
    """
    Represents a top-up product for a specific game.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='products', help_text="The game this top-up product belongs to.")
    name = models.CharField(max_length=255, help_text="Name of the top-up product (e.g., 'UC Pack 500').")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the top-up product in local currency.")
    in_game_currency = models.CharField(max_length=100, help_text="Amount or type of in-game currency (e.g., '500 UC', '1000 Diamonds').")

    class Meta:
        verbose_name = "Top-Up Product"
        verbose_name_plural = "Top-Up Products"
        unique_together = ('game', 'name') # Ensure unique product names per game
        ordering = ['game__name', 'name']

    def __str__(self):
        return f"{self.game.name} - {self.name} ({self.price} - {self.in_game_currency})"

class TopUpOrder(models.Model):
    """
    Records a top-up transaction order.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    user_email = models.EmailField(help_text="Email of the user who made the top-up order.")
    product = models.ForeignKey(TopUpProduct, on_delete=models.PROTECT, related_name='orders', help_text="The top-up product purchased.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Current status of the top-up order.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the order was created.")

    class Meta:
        verbose_name = "Top-Up Order"
        verbose_name_plural = "Top-Up Orders"
        ordering = ['-created_at'] # Order by most recent first

    def __str__(self):
        return f"Order #{self.id} - {self.user_email} - {self.product.name} ({self.status})"

