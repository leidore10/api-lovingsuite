from django.db import models
from django.contrib import admin
from django.core.validators import ValidationError
from django.db.models.base import ModelBase, subclass_exception
from django.contrib.auth.models import User
from django.apps.registry import apps
from datetime import datetime
import pdb

def imagen_user(instance,filename):
    return 'uploads/usuarios/{0}/img/{1}'.format(instance.usuario.id, filename)

# Create your models here.

class Pais(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    codigo = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    codigo = models.CharField(max_length=255, null=True)
    pais = models.ForeignKey(Pais, null=True, on_delete=models.CASCADE, related_name="provincias")

    def __str__(self):
        return self.nombre

class Localidad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    codigo_postal = models.CharField(max_length=255, null=True)
    provincia = models.ForeignKey(Provincia, null=True, on_delete=models.CASCADE, related_name="localidades")

    def __str__(self):
        return self.nombre

class Rol(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=True)
    descripcion = models.TextField(null=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super(Rol, self).save(*args, **kwargs)

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to=imagen_user,null=True)
    ubicacion = models.CharField(max_length=255, null=True)
    telefono = models.CharField(max_length=255, null=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    rol = models.ForeignKey(Rol, null=True, on_delete=models.SET_NULL, related_name="perfil_rol")

    def __str__(self):
        return str(self.id)
