from rest_framework import serializers
from .models import*


class AProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=AProduct
        fields ='__all__'