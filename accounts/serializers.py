from .models import User
from friends.models import Friend

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


class ProfileSerializer(serializers.ModelSerializer):
    friend_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["name", "reliability", "profile_img", "friend_count"]
        read_only_fields = ["reliability", "friend_count"]

    def get_friend_count(self, obj):
        return Friend.objects.filter(user=obj).count()
