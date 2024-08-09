from .models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
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
        fields = ("id", "name", "email", "password", "checkPassword")

    def validate(self, data):  # pw와 checkPw 확인
        if data["password"] != data["checkPassword"]:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["email"],
            email=validated_data["email"],
        )

        user.name = validated_data["name"]
        user.set_password(validated_data["password"])
        user.save()

        return user


# from .models import User
# from django.contrib.auth.password_validation import validate_password  # pw 검증
# from django.contrib.auth import authenticate

# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from rest_framework.validators import UniqueValidator  # 이메일 중복 방지


# # 회원가입 시리얼라이저
# class RegisterSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(
#         required=True,
#         validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복 검증
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         validators=[validate_password],
#     )
#     checkPassword = serializers.CharField(  # 비밀번호 확인
#         write_only=True,
#         required=True,
#     )

#     class Meta:
#         model = User
#         fields = ("id", "name", "email", "password", "checkPassword")

#     def validate(self, data):  # pw와 checkPw 확인
#         if data["password"] != data["checkPassword"]:
#             raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
#         return data

#     def create(self, validated_data):
#         # CREATE 요청이 들어오면 create 매서드를 오버라이딩하여 유저와 토큰 생성
#         user = User.objects.create_user(
#             username=validated_data["email"],
#             email=validated_data["email"],
#         )

#         user.name = validated_data["name"]
#         user.set_password(validated_data["password"])
#         user.save()
#         Token.objects.create(user=user)
#         # token = Token.objects.create(user=user)
#         return user


# # 로그인 시리얼라이저
# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)
#     # write_only=True 를 통해 클라이언트->서버 만 가능하도록 설정
#     password = serializers.CharField(required=True, write_only=True)

#     def validate(self, data):
#         user = authenticate(**data)
#         if user:
#             token = Token.objects.get(user=user)
#             return {
#                 "token": token.key,
#                 "user_id": user.id,
#                 "reliability": user.reliability,
#                 "profile_img_url": user.profile_img.url,
#             }

#         # 가입된 유저가 없을 경우
#         raise serializers.ValidationError({"error": "유저 정보가 존재하지 않습니다."})
