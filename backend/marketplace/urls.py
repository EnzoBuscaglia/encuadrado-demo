from django.urls import include, path
from rest_framework.routers import DefaultRouter

from marketplace.views import (
    ContentPurchaseView,
    DigitalContentViewSet,
    EventPurchaseView,
    EventViewSet,
)

router = DefaultRouter()
router.register("events", EventViewSet, basename="events")
router.register("contents", DigitalContentViewSet, basename="contents")

urlpatterns = [
    path("", include(router.urls)),
    path("purchase/event/", EventPurchaseView.as_view()),
    path("purchase/content/", ContentPurchaseView.as_view()),
]
