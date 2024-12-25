from dataclasses import field
from pydoc import classname
from rest_framework import serializers
from .models import Product
from .models import ReviewProduct



class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = ReviewProduct
        fields='__all__' 




class ProductSerializer(serializers.ModelSerializer):

    reviews = serializers.SerializerMethodField(method_name="get_review",read_only=True)
    class Meta:
        model = Product
        fields =['id','name','description','price','brand','ratings','category','stock','user','reviews']
        extra_kwargs= {
         'name': {'required': True},
         'price':{'required': True}
      }

    

    def get_review(self,obj):#obj get me current model which is product
        reviews = obj.reviews.all()
        serilaizers =ReviewSerializers(reviews,many=True)  
        return serilaizers.data 

