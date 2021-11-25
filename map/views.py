from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.core import serializers

from .models import Artist

from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from django.utils.encoding import force_text
from rest_framework import status

from rest_framework.parsers import JSONParser


class ArtistViewSet(APIView):
    queryset = Artist.objects.all()
    
    def get(self, request, format=None):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            band_name = request.data.get('name')
            if band_name:
                Artist.objects.create(name=band_name)
                return HttpResponse(status=201)
        else:
            print(serializer.errors)
            return HttpResponse(status=400)
        #drf should have a valid - check documentation
        if not isinstance( band_name, str ):
            raise ValidationError('Invalid band name', 'band_name', status_code=status.HTTP_400_BAD_REQUEST)
    
class ValidationError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'A server error occurred.'

    def __init__(self, detail, field, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_text(detail)}
        else: self.detail = {'detail': force_text(self.default_detail)}