from django.shortcuts import get_object_or_404, render_to_response, redirect, render
from django.shortcuts import render
from rest_framework import generics
from django.conf import settings
from rest_framework.views import APIView
#from rest_framework.response import Response
from django.conf import settings
from rest_framework import permissions, viewsets
from apps.core.models import *
from apps.core.serializers import *
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# Create your views here.
def index(request):
	return render(request, "index.html")