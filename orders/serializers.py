from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Order, OrderItem
from store.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_name = serializers.SerializerMethodField()
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'user_email',
            'shipping_address', 'city', 'postal_code', 'country',
            'payment_method', 'items_price', 'shipping_price', 'tax_price',
            'total_price', 'is_paid', 'paid_at', 'status', 'items', 'created_at'
        ]
        read_only_fields = ['user', 'is_paid', 'paid_at', 'status', 'created_at']

    @extend_schema_field(serializers.CharField())
    def get_user_name(self, obj):
        if obj.user.first_name and obj.user.last_name:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return obj.user.username

class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(help_text="Product database ID")
    quantity = serializers.IntegerField(min_value=1, default=1, help_text="Quantity of item to purchase")

class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField(max_length=500, help_text="Street address, apartment, suite")
    city = serializers.CharField(max_length=100, help_text="City name")
    postal_code = serializers.CharField(max_length=20, help_text="Postal / ZIP code")
    country = serializers.CharField(max_length=100, default='United States', help_text="Country name")
    payment_method = serializers.CharField(max_length=50, default='Credit Card', help_text="e.g. Credit Card, UPI / NetBanking, Cash on Delivery")
    items = OrderItemCreateSerializer(many=True, help_text="List of order items with product_id and quantity")

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')

        # Calculate prices
        items_total = 0
        order_items_to_create = []

        for item_info in items_data:
            product_id = item_info['product_id']
            qty = item_info['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} not found.")

            price = product.discount_price if product.discount_price else product.price
            items_total += price * qty

            # Deduct stock safely
            if product.stock >= qty:
                product.stock -= qty
                product.save()

            order_items_to_create.append({
                'product': product,
                'product_name': product.name,
                'product_image': product.image,
                'price': price,
                'quantity': qty
            })

        shipping_price = 0.00 if items_total >= 100 else 15.00
        tax_price = round(float(items_total) * 0.08, 2)
        total_price = float(items_total) + shipping_price + tax_price

        order = Order.objects.create(
            user=user,
            shipping_address=validated_data['shipping_address'],
            city=validated_data['city'],
            postal_code=validated_data['postal_code'],
            country=validated_data.get('country', 'United States'),
            payment_method=validated_data.get('payment_method', 'Credit Card'),
            items_price=items_total,
            shipping_price=shipping_price,
            tax_price=tax_price,
            total_price=total_price,
            is_paid=True,
            status='Processing'
        )

        for item in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                product_name=item['product_name'],
                product_image=item['product_image'],
                price=item['price'],
                quantity=item['quantity']
            )

        return order
