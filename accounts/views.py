from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes

from friends.models import Friend, FriendRequest
from .models import User

# 테스트용
from rest_framework import viewsets


@permission_classes([AllowAny])
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # jwt token 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "회원가입을 완료했습니다.",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            # jwt 토큰 => 쿠키에 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email:
            return Response({"error": "이메일을 입력하세요"}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response(
                {"error": "비밀번호를 입력하세요"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        # username에 맞는 user가 존재하지 않는 경우
        if user is None:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호가 틀린 경우,
        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # user 정보가 일치
        if user is not None:
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열화
            access_token = str(token.access_token)  # access 토큰 문자열화
            response = Response(
                {
                    "message": f"{user.name}님 안녕하세요!",
                    "user_id": user.id,
                    "reliability": user.reliability,
                    "profile_img_url": user.profile_img.url,
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."}, status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    # 로그아웃
    def delete(self, request):
        # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
        response = Response(
            {"message": "Logout success"}, status=status.HTTP_202_ACCEPTED
        )
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        return response


# jwt 토근 인증 확인용 뷰셋
# Header - Authorization : Bearer <발급받은토큰>
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


@permission_classes([IsAuthenticated])
class DeleteUserView(APIView):
    # 회원삭제
    def delete(self, request):
        # 친구 삭제
        friend = Friend.objects.filter(user=request.user)
        if friend.exists():
            friend.delete()
        reverse_friend = Friend.objects.filter(friend=request.user)
        if reverse_friend.exists():
            reverse_friend.delete()
        # 친구 요청 삭제
        friend_request = FriendRequest.objects.filter(from_user=request.user)
        if friend_request.exists():
            friend_request.delete()
        reverse_friend_request = FriendRequest.objects.filter(to_user=request.user)
        if reverse_friend_request.exists():
            reverse_friend_request.delete()

        request.user.delete()
        return Response({"message": "회원탈퇴가 완료되었습니다."}, status=status.HTTP_202_ACCEPTED)


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
