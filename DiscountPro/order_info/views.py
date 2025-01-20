from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Order
from .serializers import OrderSerializer
from discount_info.models import Discount

@api_view(['GET', 'POST'])
def order_list(request):
    """
    List all orders or create a new order
    """
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            # breakpoint()
            try:
                with transaction.atomic():
                    order = serializer.save()
                return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def order_detail(request, pk):
    """
    Retrieve, update or delete an order
    """
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    order = serializer.save()
                return Response(OrderSerializer(order).data)
            except Exception as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def apply_discount_to_order(request, pk):
    """
    Apply a discount to an existing order
    """
    order = get_object_or_404(Order, pk=pk)
    discount_id = request.data.get('discount_id')
    
    if not discount_id:
        return Response(
            {'error': 'discount_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    discount = get_object_or_404(Discount, pk=discount_id)
    
    if not discount.is_active:
        return Response(
            {'error': 'Discount is not active'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    order.applied_discount = discount
    order.calculate_totals()
    
    return Response(OrderSerializer(order).data)