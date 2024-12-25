from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .models import Product, ReviewProduct
from .serializers import ProductSerializer
from rest_framework.response import Response
from .filter import ProductFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Avg

#create product
@api_view(["POST"])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    data =  request.data
    serializer = ProductSerializer(data=data)
    if serializer.is_valid():
        product = Product.objects.create(**data,user = request.user)

        res = ProductSerializer(product,many=False)
        return Response({"product":res.data})
    else:
        return Response(serializer.errors)




@api_view(['GET'])
def get_products(request):
    # Apply filters to the queryset
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    # print("filter",filterset)
    # print("filte qsr",filterset.qs)

    # Check if filterset is valid
    if not filterset.is_valid():
        return Response({"errors": filterset.errors}, status=400)
    
         #pagination
    perpage = 100
    paginator = PageNumberPagination()
    paginator.page_size = perpage
    query_set = paginator.paginate_queryset(filterset.qs,request)

    # Serialize the filtered queryset
    serializer = ProductSerializer(query_set, many=True)
    
    return Response({"products": serializer.data,
    "resultperpage":perpage,
    "count":count
    })


@api_view(['GET'])
def get_product(request,pk):
    product = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(product,many= False)
    return Response({'product':serializer.data}) 


@api_view(["PUT"])
@permission_classes([IsAuthenticated,IsAdminUser])
def product_update(request,pk):
    product = get_object_or_404(Product,id=pk)
    print("product",request.user)
    if product.user != request.user:
        return Response({"message":"unautherization"})
    product.name = request.data["name"]
    product.description = request.data["description"]
    product.brand = request.data["brand"]
    product.price = request.data["price"]
    product.ratings = request.data["ratings"]
    product.save()

    res = ProductSerializer(product,many=False)
    return Response({"product":res.data})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_product(request,pk):
     product = Product.objects.get(id = pk)
     if product.user != request.user:
        return Response({"message":"unautherization"})
     product.delete()   
     return Response({"delete_product":"deleted"},status = status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    user = request.user
    product = get_object_or_404(Product,id = pk)
    data = request.data

    review = product.reviews.filter(user = user)
    if data['rating'] >5 or data['rating']<=0:
        return Response({"eeror":"please rate between 1- 5"},status = status.HTTP_400_BAD_REQUEST)
    

    elif review.exists():
        new_review = {'rating':data['rating'],'comment':data['comment']}
        review.update(**new_review)
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.ratings = rating['avg_rating']
        product.save()
        return Response({"review":"review updated"})
    else:
        ReviewProduct.objects.create(
             user = user,
             comment = data["comment"],
             rating = data["rating"],
             product = product
         )   
        
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        product.ratings = rating['avg_rating']
        product.save()
        return Response({"created new review"})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):

    product = get_object_or_404(Product,id=pk)
    user = request.user
    review= product.reviews.filter(user=user)
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_rating = Avg('rating'))
        if rating['avg_rating'] is None:
            rating['avg_rating'] =0
        product.ratings = rating['avg_rating']
        product.save()
        return Response({"review":"deleted"})
    else:
        return Response({"error":"not found"},status = status.HTTP_404_NOT_FOUND)




