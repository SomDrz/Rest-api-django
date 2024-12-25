from dataclasses import field
from rest_framework import serializers
from django.contrib.auth.models import User


class SingnUpSerializers(serializers.ModelSerializer):  #for signup
    class Meta:
        model = User
        fields=["first_name","last_name","email","password"]
        extra_kwargs= {
         'first_name': {'required': True},
         'last_name':{'required': True},
         'email':{'required': True},
         'password':{'required': True,'min_length':6}
      }
class UserSerializers(serializers.ModelSerializer):  # this we use to display the user
    class Meta:
        model = User
        fields=["first_name","last_name","email","username"]
