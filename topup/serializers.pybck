from rest_framework import serializers
from .models import Game, TopUpProduct, TopUpOrder

class TopUpRequestSerializer(serializers.Serializer):
    """
    Serializer for the incoming POST request to /api/topup/.
    This is not directly tied to a model.
    """
    gamename = serializers.CharField(max_length=255)
    game_id = serializers.CharField(max_length=100)
    product_name = serializers.CharField(max_length=255)
    product_id = serializers.IntegerField() # This will be the TopUpProduct's primary key
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2) # For validation consistency
    user_email = serializers.EmailField()
    payment_status = serializers.CharField(max_length=20) # Will be 'pending' initially

    def validate(self, data):
        """
        Custom validation to check game activity and product association.
        """
        gamename = data.get('gamename')
        game_id = data.get('game_id')
        product_name = data.get('product_name')
        product_id = data.get('product_id')
        product_price = data.get('product_price')

        # 1. Validate Game exists and is active
        try:
            game = Game.objects.get(game_id=game_id, name=gamename)
            if not game.is_active:
                raise serializers.ValidationError("The specified game is currently inactive.")
        except Game.DoesNotExist:
            raise serializers.ValidationError("Game with provided name and ID does not exist.")

        # 2. Validate TopUpProduct exists and is associated with the game
        try:
            # Using game.products.get for efficient querying and implicitly checking association
            product = game.products.get(id=product_id, name=product_name)
            # Optional: Add a check for price consistency if needed
            if product.price != product_price:
                 # This could be a warning or a strict error depending on business logic
                print(f"Warning: Product price mismatch for {product_name}. Expected {product.price}, got {product_price}.")
                # raise serializers.ValidationError(f"Product price mismatch. Expected {product.price}, got {product_price}.")
        except TopUpProduct.DoesNotExist:
            raise serializers.ValidationError("Product with provided name and ID is not found or not associated with the specified game.")

        # Store the validated product object for easier access in create method
        data['product_instance'] = product
        return data

class TopUpOrderSerializer(serializers.ModelSerializer):
    """
    Model serializer for the TopUpOrder.
    Used for creating and representing TopUpOrder instances.
    """
    class Meta:
        model = TopUpOrder
        fields = ['id', 'user_email', 'product', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

