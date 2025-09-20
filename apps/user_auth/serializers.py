from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as DjoserUserSerializers

User = get_user_model()


class UserCreateSerializer(DjoserUserSerializers):
    class Meta(DjoserUserSerializers.Meta):
        model = User
        fields = [
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "id_no",
            "security_question",
            "security_answer",
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user
