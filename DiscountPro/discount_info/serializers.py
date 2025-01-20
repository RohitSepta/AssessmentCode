from rest_framework import serializers
from .models import PercentageDiscount, FixedDiscount, Discount


class PercentageDiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PercentageDiscount
        fields = ['percentage', 'min_purchase_amount']

class FixedDiscountDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedDiscount
        fields = ['amount', 'min_purchase_amount']

class DiscountSerializer(serializers.ModelSerializer):
    percentage_discount = PercentageDiscountDetailSerializer(required=False)
    fixed_discount = FixedDiscountDetailSerializer(required=False)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = [
            'id', 'name', 'description', 'discount_type',
            'is_active', 'start_date', 'end_date',
            'percentage_discount', 'fixed_discount',
            'discounted_price', 'created_at', 'updated_at'
        ]

    def get_discounted_price(self, obj):
        price = self.context.get('price', 0)
        return obj.apply_discount(price)

    def create(self, validated_data):
        discount_type = validated_data.get('discount_type')
        percentage_data = validated_data.pop('percentage_discount', None)
        fixed_data = validated_data.pop('fixed_discount', None)

        discount = Discount.objects.create(**validated_data)

        if discount_type == 'percentage' and percentage_data:
            PercentageDiscount.objects.create(discount=discount, **percentage_data)
        elif discount_type == 'fixed' and fixed_data:
            FixedDiscount.objects.create(discount=discount, **fixed_data)

        return discount