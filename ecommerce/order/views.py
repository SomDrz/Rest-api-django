
from asyncio.windows_events import NULL
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from product.models import Product
from .serializers import OrderSerializer
from rest_framework.response import Response
# from .filter import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import Order, OrderItem
from django.db import transaction





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data

    order_items = data.get('orderItems', [])
    if not order_items or len(order_items) == 0:
        return Response({"detail": "Add at least one product."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            # Calculate the total amount
            total_amount = sum(item['price'] * item['quantity'] for item in order_items)

            # Create the order
            order = Order.objects.create(
                user=user,
                street=data["street"],
                city=data["city"],
                state=data["state"],
                zip_code=data["zip_code"],
                phone_no=data["phone_no"],
                country=data["country"],
                total_amount=total_amount
            )

            # Create order items and update stock
            for i in order_items:
                try:
                    product = Product.objects.get(id=i['product'])
                except Product.DoesNotExist:
                    return Response({"detail": f"Product with ID {i['product']} not found."}, status=status.HTTP_404_NOT_FOUND)

                # Check stock availability
                if product.stock < i['quantity']:
                    return Response({"detail": f"Not enough stock for product '{product.name}'."}, status=status.HTTP_400_BAD_REQUEST)

                # Create order item
                item = OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    quantity=i['quantity'],
                    price=i['price']
                )

                # Update product stock
                product.stock -= item.quantity
                product.save()

            # Serialize the created order
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_order(request):
    order = Order.objects.all()
    serializer = OrderSerializer(order,many = True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    serializer = OrderSerializer(order,many = False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request,pk):
    order = get_object_or_404(Order, id=pk).delete()
    return Response({f"order deleted {pk}:{order}"})



@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request, pk):
    
    order = get_object_or_404(Order, id=pk)
    order.status = request.data.get("status")
    order.save()
    serializer = OrderSerializer(order,many = False)
    return Response(serializer.data)

