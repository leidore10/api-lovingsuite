from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from apps.core.models import *
from apps.utils import *
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


import pdb

# Create your views here.
class UserAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})

        if serializer.is_valid() != True:
            return Response({
                'detail': 'Login Error: Incorrect username or password1',
                'errors': serializer.errors
            })
        serializer.is_valid(raise_exception=True)
        #pdb.set_trace()
        user = serializer.validated_data['user']

        payload = jwt_payload_handler(user)
        tokenJWT = jwt_encode_handler(payload)

        login = False
        queryset = Perfil.objects.filter(usuario=user.id)

        if tokenJWT and queryset.count() > 0:
            login = True
            role = queryset.first().rol

        if login == True:
            return Response({
                'token': tokenJWT,
                'id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': role.code
            })
        else:
            return Response({
                'detail': 'Login Error: Incorrect username or password2',
                'errors': serializer.errors
            })