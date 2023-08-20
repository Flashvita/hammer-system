import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


class InviteCode(models.Model):
    user = models.OneToOneField(
        to="User",
        on_delete=models.CASCADE,
        verbose_name=_("user invite code"),
        related_name="invite_code"
    )
    code = models.CharField(verbose_name=_("code"), max_length=6,  unique=True, db_index=True)
    users_activate_invite = models.ManyToManyField(
        to="User",
        default=None,
        verbose_name=_("Users activated my invite code"),
        related_name="invited_users"
    )

    def save(self, **kwargs) -> None:
        self.code = f"{uuid.uuid4()}"[0:6]
        return super().save(**kwargs)
    

class User(AbstractUser):
    username = PhoneNumberField(
        # https://django-phonenumber-field.readthedocs.io/en/latest/reference.html#model-field
        verbose_name=_("Phone number"),
        unique=True,
    )
    
    @property
    def activated_invite_code(self) -> InviteCode:
        return InviteCode.objects.prefetch_related("users_activate_invite").filter(
            users_activate_invite=self)

    @property
    def users_activated_my_invite_code(self) -> list:
        return list(InviteCode.objects.prefetch_related("users_activate_invite").select_related("user").get(user=self).users_activate_invite.all().values_list("username", flat=True))
        #return list(self.invite_code.users_activate_invite.all().values_list("user__username", flat=True))
    
    @property
    def my_invite_code(self) -> str:
        #invite_code = self.activated_invite_code
        return self.invite_code.code if self.invite_code else ""

    def __str__(self) -> str:
        return f"{self.username}"
    
    class Meta(AbstractUser.Meta):
        # Comes from original Django Auth declaration
        swappable = "AUTH_USER_MODEL"

    