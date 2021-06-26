from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction
from rest_framework.response import Response
from apps.utils import UtilClass
import pdb

class RolSerializer(serializers.ModelSerializer):
    next_id = serializers.SerializerMethodField(read_only=True)
    def get_next_id(self, obj):
        return UtilClass.next_id(self.Meta.model, obj.id)
    previous_id = serializers.SerializerMethodField(read_only=True)
    def get_previous_id(self, obj):
        return UtilClass.previous_id(self.Meta.model, obj.id)
    class Meta:
        model = Rol
        fields = '__all__'

class PerfilSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False, use_url=False)
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Perfil
        fields = '__all__'

class LocalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localidad
        fields = '__all__'

class ProvinciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provincia
        fields = '__all__'

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = PerfilSerializer(read_only=True)

    next_id = serializers.SerializerMethodField(read_only=True)
    def get_next_id(self, obj):
        return UtilClass.next_id(self.Meta.model, obj.id)
    previous_id = serializers.SerializerMethodField(read_only=True)
    def get_previous_id(self, obj):
        return UtilClass.previous_id(self.Meta.model, obj.id)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True, 'required': False}}
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        try:
            with transaction.atomic():
                user.save()
        except DatabaseError:
            user = None
        if user:
            profile_data = self.context.get('request').data.get('profile')
            rol = self.context.get('request').data.get('rol', None)
            if profile_data:
                profile = Perfil.objects.create(
                    usuario = user,
                    image = profile_data.get('image', None),
                    ubicacion = profile_data.get('ubicacion', None),
                    telefono = profile_data.get('telefono', None)
                )
            else:
                profile = Perfil.objects.create(
                    usuario = user
                )
            if rol:
                profile.rol = Rol.objects.get(pk=int(rol.get('id')))
                profile.save()

        return user


    def update(self, instance, validated_data):
        profile_data = self.context.get('request').data.get('profile')
        if validated_data.get('password'):
            instance.set_password(validated_data['password'])
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()

        if profile_data:
            profile = Perfil.objects.filter(usuario=User.objects.get(pk=instance.id))
            if profile.first():
                profile = profile.first()
                if profile_data.get('image', None):
                    profile.image = profile_data.get('image', None)
                profile.ubicacion = profile_data.get('ubicacion', None)
                profile.telefono = profile_data.get('telefono', None)
            else:
                profile = Perfil.objects.create(
                    usuario = instance,
                    image = profile_data.get('image', None),
                    ubicacion = profile_data.get('ubicacion', None),
                    telefono = profile_data.get('telefono', None)
                )
            profile.save()

        rol = self.context.get('request').data.get('rol', None)
        if rol:
            profile.rol = Rol.objects.get(pk=int(rol.get('id')))
            profile.save()
        return instance