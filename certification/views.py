from django.shortcuts import render
from django.http import HttpResponse
from .models import Block

# Create your views here.

def index(request):
	return render(request, 'user.html')

def blocks(request):
	return render(request, 'user.html')

def block(request):
	return render(request, 'user.html')

def user(request):
	images = Block.objects.filter(validator__name="University",student=request.user.student)
	return render(request, 'user.html',{'images':images})


