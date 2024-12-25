from django.urls import path,include
from . import views


urlpatterns = [
    path('register/',views.register_user,name="register_user"),
    path('me/',views.current_user,name="current_user"),
    path('me/update/',views.user_update,name="user_update"),
    path('forgot_password/',views.forgot_password,name="forgot_password"),
    path('reset_password/<str:token>',views.reset_password,name="reset_password")


]

