from rest_framework import serializers
from .models import Review, Reply, Recommend


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = "__all__"


class RecommendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommend
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    replies_count = serializers.IntegerField(source="replies.count", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "user_name",
            "content",
            "recommend_count",
            "decommend_count",
            "date",
            "replies_count",
        ]


class ReplyListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)

    class Meta:
        model = Reply
        fields = [
            "id",
            "user_name",
            "content",
            "date",
        ]
