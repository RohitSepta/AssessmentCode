from rest_framework import serializers
from .models  import SeasonalProduct, BulkProduct, Product



class SeasonalProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalProduct
        fields = ['season', 'season_discount', 'off_season_discount']

class BulkProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkProduct
        fields = ['min_quantity', 'bulk_discount']

class ProductSerializer(serializers.ModelSerializer):
    seasonal_details = SeasonalProductDetailSerializer(required=False)
    bulk_details = BulkProductDetailSerializer(required=False)
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'base_price', 
            'product_type', 'seasonal_details', 'bulk_details',
            'final_price', 'created_at', 'updated_at'
        ]

    def get_final_price(self, obj):
        try:
            quantity = self.context.get('quantity', 1)
            if obj.product_type == 'seasonal':
                discount = obj.seasonal_details.get_current_discount()
                return float(obj.base_price) * (1 - discount)
            elif obj.product_type == 'bulk':
                if quantity >= obj.bulk_details.min_quantity:
                    return float(obj.base_price) * (1 - float(obj.bulk_details.bulk_discount))
            return float(obj.base_price)
        except Exception:
            return float(obj.base_price)

    def create(self, validated_data):
        product_type = validated_data.get('product_type')
        seasonal_details = validated_data.pop('seasonal_details', None)
        bulk_details = validated_data.pop('bulk_details', None)

        product = Product.objects.create(**validated_data)

        if product_type == 'seasonal' and seasonal_details:
            SeasonalProduct.objects.create(product=product, **seasonal_details)
        elif product_type == 'bulk' and bulk_details:
            BulkProduct.objects.create(product=product, **bulk_details)

        return product