from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.shortcuts import render
from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
#from rest_framework.response import Response
from django.conf import settings
from rest_framework import permissions, viewsets
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from rest_framework.decorators import action, api_view
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import pdb

# Create your views here.
class ApiPublic:

    def getSome(self):
        return True