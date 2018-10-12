from rest_framework import serializers
from .models import TA

class TASerializer(serializers.ModelSerializer):

    class Meta:
        model = TA
        fields = '__all__'
