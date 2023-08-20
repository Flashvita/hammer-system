import random
import string

from django.core.cache import cache
from django.conf import settings
from django.db import transaction

from rest_framework import exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from time import sleep

from account.models import User, InviteCode


def make_send_sms(data: dict) -> dict:
    sleep(2) # For imitate integration for sms service
    code = generate_code()
    cache.set(
                f"{data['phone_number']}-verify-code",
                code,
                settings.VERIFY_CODE_TIMEOUT
            )
    return {"phone_number": data['phone_number'], "code": code}


def verify_input_code(data: dict) -> bool:
    return data['code'] == cache.get(f"{data['phone_number']}-verify-code")


def generate_code(digits_count: int = settings.ACCOUNT_VERIFICATION_CODE_DIGITS_COUNT) -> str:
    return "".join(
        random.SystemRandom().choice(string.digits) for _ in range(digits_count)
    )


def create_token(user) -> dict:
    refresh = RefreshToken.for_user(user)
    return {
                "refresh": f"{refresh}",
                "access": f"{refresh.access_token}",
            }	


def user_registration_flow(data: dict) -> dict:
    with transaction.atomic():
        try:    
            if not verify_input_code(data):
                raise exceptions.ValidationError("Input code invalid or expired")
            user = User.objects.create(username=data['phone_number'])
            user.set_password(data['password'])
            user.save(update_fields=["password"])
            InviteCode.objects.create(user=user)
            token_data = create_token(user)
        except Exception as e:
            raise exceptions.ValidationError(e.args[0])
    return token_data


def update_invite_code(user, input_code: str) -> dict:
    if InviteCode.objects.filter(code=input_code).exists():
        if not user.activated_invite_code:
            invite_code = InviteCode.objects.get(code=input_code)
            invite_code.users_activate_invite.add(user)
            return {"success": True}
        raise exceptions.PermissionDenied("Forbidden to activate more one invite code")
    raise exceptions.NotFound("Not found input code")
     