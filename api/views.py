from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TA
from .serializers import TASerializer

class TAPlots(APIView):
    def get(self):
        plots = TA.objects.all()
        serializer = TASerializer(plots, many=True)
        return Response(serializer.data)
