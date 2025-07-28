from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from marketplace.models import ContentDownload, Customer, EventRegistration, PaymentStatus
from model.models import DigitalContent, DiscountCode, Event

from .serializers import (
    ContentDownloadCreateSerializer,
    DigitalContentSerializer,
    EventRegistrationCreateSerializer,
    EventSerializer,
)


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class DigitalContentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DigitalContent.objects.all()
    serializer_class = DigitalContentSerializer


class EventPurchaseView(APIView):
    def post(self, request):
        serializer = EventRegistrationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        customer, _ = Customer.objects.get_or_create(
            email=data["email"], defaults={"name": data["name"]}
        )
        event = get_object_or_404(Event, id=data["event_id"])
        discount = DiscountCode.objects.filter(
            code=data.get("discount_code", ""), is_active=True
        ).first()

        normal_price = event.price
        discount_amount = (discount.discount_percentage * normal_price // 100) if discount else 0
        final_price = normal_price - discount_amount

        if data["payment_method"] == "card" and final_price % 10 >= 8:
            status_ = PaymentStatus.FAILED
            paid_at = None
        else:
            status_ = PaymentStatus.PAID
            paid_at = now()

        EventRegistration.objects.create(
            customer=customer,
            event=event,
            normal_price=normal_price,
            final_price=final_price,
            discount_code=discount,
            payment_status=status_,
            paid_at=paid_at,
        )

        return Response({"status": status_}, status=status.HTTP_200_OK)


class ContentPurchaseView(APIView):
    def post(self, request):
        serializer = ContentDownloadCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        customer, _ = Customer.objects.get_or_create(
            email=data["email"], defaults={"name": data["name"]}
        )

        content = get_object_or_404(DigitalContent, id=data["content_id"])
        discount = DiscountCode.objects.filter(
            code=data.get("discount_code", ""), is_active=True
        ).first()

        normal_price = content.price
        discount_amount = (discount.discount_percentage * normal_price // 100) if discount else 0
        final_price = normal_price - discount_amount

        if data["payment_method"] == "card" and final_price % 10 >= 8:
            status_ = PaymentStatus.FAILED
            paid_at = None
        else:
            status_ = PaymentStatus.PAID
            paid_at = now()

        ContentDownload.objects.create(
            customer=customer,
            content=content,
            normal_price=normal_price,
            final_price=final_price,
            discount_code=discount,
            payment_status=status_,
            paid_at=paid_at,
        )

        return Response({"status": status_}, status=status.HTTP_200_OK)
