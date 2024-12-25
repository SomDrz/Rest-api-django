from django.urls import path
from . import views




urlpatterns = [
    path('products/',views.get_products,name="paroducts"),
    path('product/newproduct/',views.new_product,name="new_product"),
    path('product/<str:pk>',views.get_product,name="get_product_details"),
    path('product/<int:pk>/update/',views.product_update,name="product_update"),
    path('product/<int:pk>/delete/',views.delete_product,name="delete_product"),
    path('<str:pk>/review/',views.create_review,name="create_review"),
    path('<str:pk>/review/delete',views.delete_review,name="delete_review")
     
]
