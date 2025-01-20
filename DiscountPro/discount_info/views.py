from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Discount
from .serializers import DiscountSerializer


@api_view(['GET', 'POST'])
def discount_list(request):
    """
    List all discounts or create a new discount
    """
    if request.method == 'GET':
        discounts = Discount.objects.all()
        price = request.query_params.get('price', 0)
        serializer = DiscountSerializer(discounts, many=True, context={'price': float(price)})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def discount_detail(request, pk):
    """
    Retrieve, update or delete a discount
    """
    discount = get_object_or_404(Discount, pk=pk)

    if request.method == 'GET':
        price = request.query_params.get('price', 0)
        serializer = DiscountSerializer(discount, context={'price': float(price)})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def calculate_discount(request, pk):
    """
    Calculate discounted price for a given price
    """
    discount = get_object_or_404(Discount, pk=pk)
    price = float(request.query_params.get('price', 0))
    
    discounted_price = discount.apply_discount(price)
    savings = price - discounted_price
    
    return Response({
        'discount_name': discount.name,
        'original_price': price,
        'discounted_price': discounted_price,
        'savings': savings,
        'discount_type': discount.discount_type
    })