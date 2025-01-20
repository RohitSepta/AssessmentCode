from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer

@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all products or create a new product
    """
    if request.method == 'GET':
        products = Product.objects.all()
        quantity = request.query_params.get('quantity', 1)
        serializer = ProductSerializer(products, many=True, context={'quantity': int(quantity)})
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    """
    Retrieve, update or delete a product
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        quantity = request.query_params.get('quantity', 1)
        serializer = ProductSerializer(product, context={'quantity': int(quantity)})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def calculate_price(request, pk):
    """
    Calculate final price for a product
    """
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.query_params.get('quantity', 1))
    
    serializer = ProductSerializer(product, context={'quantity': quantity})
    
    return Response({
        'product': product.name,
        'base_price': float(product.base_price),
        'quantity': quantity,
        'final_price': serializer.data['final_price'],
        'total_price': serializer.data['final_price'] * quantity
    })