from .models import User
from django.contrib.auth.password_validation import validate_password  # pw 검증

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator  # 이메일 중복 방지


# 회원가입 시리얼라이저
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    checkPassword = serializers.CharField(  # 비밀번호 확인
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ("id", "email", "password", "checkPassword")

    def validate(self, data):  # pw와 checkPw 확인
        if data["password"] != data["checkPassword"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        # CREATE 요청이 들어오면 create 매서드를 오버라이딩하여 유저와 토큰 생성
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["email"],
        )

        # 초기 닉네임 설정: USER + id
        if not user.nickname:
            user.nickname = f"USER{user.id}"

        user.set_password(validated_data["password"])
        user.save()
        Token.objects.create(user=user)
        # token = Token.objects.create(user=user)
        return user
