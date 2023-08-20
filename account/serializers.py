from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from account.models import User


class PhoneNumberSerializer(serializers.Serializer):
    # https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#serializer-field
    phone_number = PhoneNumberField()


class CreateUserSerializer(PhoneNumberSerializer):
    code = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class UserProfileProfileSerializer(UserSerializer):
    code = serializers.SerializerMethodField()
    invited_users = serializers.SerializerMethodField()

    def get_code(self, obj):
            return obj.my_invite_code
    
    def get_invited_users(self, obj):
        return obj.users_activated_my_invite_code

    class Meta(UserSerializer.Meta):
        fields = ("username", "code", "invited_users",
                  "first_name", "last_name", "id"
                )


class UserListSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = ("username", "id")
    

class InviteCodeSerializer(serializers.Serializer):
    code = serializers.CharField()
    
    def validate_code(self, code):
        if 6 == len(code) and code.isalnum():
            return code
        raise serializers.ValidationError("Invalid code")
