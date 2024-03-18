from payment import views
from rest_framework.routers import DefaultRouter

app_name = 'payment'

router = DefaultRouter()

router.register(r'reason', views.ReasonViewSet, basename='reason')
router.register(r'attendee', views.AttendeeViewSet, basename='attendee')

urlpatterns = router.urls
