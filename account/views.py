
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import exceptions, status
from rest_framework.permissions import IsAuthenticated, AllowAny

from drf_yasg.utils import swagger_auto_schema

from account.serializers import (
    PhoneNumberSerializer,
    CreateUserSerializer,
    UserListSerializer,
    UserProfileProfileSerializer,
    InviteCodeSerializer
    )
from account.services import (
    make_send_sms,
    user_registration_flow,
    update_invite_code
    )
from account.models import User


class UserViewSet(RetrieveModelMixin,
                   ListModelMixin,
                   GenericViewSet):
    queryset = User.objects.filter(is_superuser=False)
    http_method_names = ["post", "get", "patch"]
    
  
    def get_permissions(self):
        if self.action == "activate_invite_code":
            return [IsAuthenticated()]
        else:
            return [AllowAny()]
        
    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.select_related("invite_code")
        else:
            return self.queryset
    
    def get_serializer_class(self):
        if self.action == "register":
            return CreateUserSerializer
        if self.action == "send_sms":
            return PhoneNumberSerializer
        if self.action == "retrieve":
            return UserProfileProfileSerializer
        if self.action == "list":
            return UserListSerializer
        if self.action == "activate_invite_code":
            return InviteCodeSerializer

    @swagger_auto_schema(operation_description='POST /send-sms')
    @action(methods=["post"], detail=False)
    def send_sms(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            return Response(make_send_sms(serializer.data), status=status.HTTP_201_CREATED)
        raise exceptions.ValidationError(f"Invalid phone number: {serializer.data['phone_number']}")
    
    @swagger_auto_schema(operation_description='POST /register')
    @action(methods=["post"], detail=False)
    def register(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer_class()(data=request.data)
            if serializer.is_valid():
                return Response(user_registration_flow(serializer.validated_data), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description='PATCH /activate-invite-code')
    @action(methods=["patch"], detail=False, permission_classes=[IsAuthenticated])
    def activate_invite_code(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            update_invite_code(request.user, serializer.validated_data['code'])
            return Response(status=status.HTTP_200_OK)
        raise exceptions.ValidationError(f"Invalid input invite code {serializer.errors}")
    
    