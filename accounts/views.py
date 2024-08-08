# from django.shortcuts import render
from .models import User
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from rest_framework.decorators import api_view

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            return Response(
                {
                    "token": validated_data["token"],
                    "user_id": validated_data["user_id"],
                    "reliability": validated_data["reliability"],
                    "profile_img_url": validated_data["profile_img_url"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def profile(request):
    user = User.objects.get(id=21)  # 임시 유저 지정
    # user = request.user

    if request.method == "GET":
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"error": "Unsupported method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
