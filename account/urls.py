
from rest_framework import routers
from account.views import UserViewSet
router = routers.SimpleRouter(trailing_slash=False)
router.register(r'account', UserViewSet)
#router.get_default_basename = "/"

urlpatterns = router.urls
