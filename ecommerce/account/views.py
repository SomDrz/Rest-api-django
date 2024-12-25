from datetime import datetime, timedelta
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .serializers import SingnUpSerializers, UserSerializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.core.mail import  send_mail

@api_view(["POST"])
def register_user(request):
    data = request.data
    user = SingnUpSerializers(data=data)
    if user.is_valid():
        if not User.objects.filter(username=data["email"]).exists():
            user = User.objects.create(
                first_name = data["first_name"],
                last_name = data["last_name"],
                email = data["email"],
                username = data["email"],
                password =make_password( data["password"])
            )
            return Response({"USER":"user CREATED "},status = status.HTTP_201_CREATED)

        else:
            return Response({"error":"user exits already"},status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(user.errors)           




@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    print("curent_user",request.user) # all user data inside user
    user = UserSerializers(request.user)
    return Response(user.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def user_update(request):
    user = request.user
    user.first_name = request.data["first_name"]
    user.last_name = request.data["last_name"]
    user.email = request.data["email"]

    if request.data["password"] != "":
        user.password = make_password(request.data["password"])

    serializers = SingnUpSerializers(user,many=False)
    return  Response({"data": serializers.data})


def  get_current_host(request):
    protocol  = request.is_secure() and 'http' or 'https'
    host = request.get_host()
    return "{protocol}://{host}/".format(protocol=protocol,host=host)



@api_view(['POST'])
def forgot_password(request):
    data = request.data
    user  = get_object_or_404(User,email = data['email'])
    token = get_random_string(40)
    expire_date= datetime.now()+timedelta(minutes=30)
    print("hi",user.profile.reset_password_token)
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date


    user.profile.save()
    host = get_current_host(request)
    link = "{host}/api/Reset_password/{token}".format(host = host,token = token)
    body ="your password link: {link}".format(link=link) 
    send_mail(
        "password reset for ecommerce",
        body,
        "noreply@ecommerce.com",
        [data['email']]
    )
    return Response({'detail':"password reset: {email}".format(email=data['email'])})

@api_view(['POST'])
def reset_password(request,token):
    data = request.data
    user  = get_object_or_404(User,profile__reset_password_token = token)
    
    if user.profile.reset_password_expire.replace(tzinfo =None) < datetime.now():
        return Response({"timeout try again"})
    if data["password"] != data["confirmpassword"]:
        return Response({"password are not same"})
    user.password = make_password(data["password"]) 
    user.profile.reset_password_token=""
    user.reset_password_expire = None
    user.profile.save()
    user.save()
    return Response({"password reset sucessfully"})


