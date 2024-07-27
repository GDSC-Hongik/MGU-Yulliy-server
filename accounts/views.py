# from django.shortcuts import render
from .models import User
from rest_framework import generics

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
