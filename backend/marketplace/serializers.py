from rest_framework import serializers

from marketplace.models import Customer
from model.models import DigitalContent, Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "description", "start_time", "duration", "price", "is_online"]


class DigitalContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalContent
        fields = ["id", "name", "description", "price"]


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["name", "email"]


class EventRegistrationCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    event_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=["card", "other"])
    discount_code = serializers.CharField(required=False, allow_blank=True)


class ContentDownloadCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    content_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(choices=["card", "other"])
    discount_code = serializers.CharField(required=False, allow_blank=True)
