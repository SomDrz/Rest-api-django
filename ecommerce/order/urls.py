from django.urls import path
from . import views




urlpatterns = [
    path('neworder/',views.new_order,name="new_order"),
    path('getAllOrder/',views.get_all_order,name="get_all_order"),
    path('order/<str:pk>/update/',views.process_order,name="process_order"),
    path('order/<str:pk>/delete/',views.delete_order,name="delete_order")     
]
