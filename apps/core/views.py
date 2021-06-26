from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import *
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.decorators import action
from api.paginator import StandardResultsSetPagination
from django.db import DatabaseError, transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from rest_framework.parsers import JSONParser
from django.db import DatabaseError, transaction, IntegrityError
from django.db import models
import pdb

from apps.utils import NestedMultipartParser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().exclude(username='super')
    serializer_class = UserSerializer
    parser_classes = (JSONParser, NestedMultipartParser)
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        filter = request.GET.get('_q')
        if filter:
            self.queryset = self.queryset.filter((Q(first_name__icontains=filter) | Q(last_name__icontains=filter) | Q(email__icontains=filter)))
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    def create(self, request):
        instance = None
        id = request.data.get('id', None)
        #pdb.set_trace()
        if id:
            instance = User.objects.get(pk=id)
        serializer = self.serializer_class(data=request.data, instance=instance, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                user = User.objects.get(pk=user.id)
                return Response(self.serializer_class(user).data)
            else:
                return Response({
                    'success': False
                })
        else:
            return Response({
                'success': False,
                'message': serializer.errors
            })

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

class PaisViewSet(viewsets.ModelViewSet):
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

class ProvinciaViewSet(viewsets.ModelViewSet):
    queryset = Provincia.objects.all()
    serializer_class = ProvinciaSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    @action(detail=True, methods=['get'])
    def pais(self, request, pk=None):
        result = []
        if not pk:
            return JsonResponse(result)
        provincias = Provincia.objects.filter(pais=pk).order_by('nombre')
        return Response(self.serializer_class(provincias, many=True).data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

class LocalidadViewSet(viewsets.ModelViewSet):
    queryset = Localidad.objects.all()
    serializer_class = LocalidadSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    @action(detail=True, methods=['get'])
    def provincia(self, request, pk=None):
        result = []
        if not pk:
            return JsonResponse(result)
        lodalidades = Localidad.objects.filter(provincia=pk).order_by('nombre')
        return Response(self.serializer_class(lodalidades, many=True).data)

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

    @action(detail=True, methods=['get'])
    def localidades(self, request, pk=None):
        if request.method == 'GET':
            if not pk:
                return JsonResponse({"detail" : "failure"})
            localidades = []
            for item in pk.split(','):
                localidades.append(Localidad.objects.get(pk=item))
        return Response(self.serializer_class(localidades, many=True).data)

    @action(detail=True, methods=['get'])
    def provincia(self, request, pk=None):
        if request.method == 'GET':
            if not pk:
                return JsonResponse({"detail" : "failure"})
            localidades = Localidad.objects.filter(provincia=pk)
            if localidades.count() == 0:
                return JsonResponse({"detail" : "failure"})
            result = []
            for item in localidades:
                data = {
                    "id": item.id,
                    "nombre": item.nombre,
                    "provincia": item.provincia.id
                }
                result.append(data)
        return JsonResponse(result, safe=False)

class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    pagination_class = StandardResultsSetPagination

    def list(self, request):
        page = self.paginate_queryset(self.queryset)
        serializer_element = self.serializer_class(page, many=True)
        return self.get_paginated_response(serializer_element.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.delete():
            return Response({"detail" : "success"})

    @action(detail=False, methods=['get'])
    def all(self, request):
        return Response(self.serializer_class(self.queryset, many=True).data)

"""
def list(self, request):
    pass

def create(self, request):
    pass

def retrieve(self, request, pk=None):
    pass

def update(self, request, pk=None):
    pass

def partial_update(self, request, pk=None):
    pass

def destroy(self, request, pk=None):
    pass
"""



