from django.shortcuts import render
from payment.serializers import (AccountSerializer, AttendeeSerializer,
                                 ActionSerializer, PaymentSerializer,
                                 CollectSerializer, ReasonSerializer)
from payment.models import Attendee, Account, Action, Payment, Reason, Collect
from rest_framework import viewsets

class ReasonViewSet(viewsets.ModelViewSet):
    serializer_class = ReasonSerializer
    queryset = Reason.objects.all()


class AttendeeViewSet(viewsets.ModelViewSet):
    serializer_class = AttendeeSerializer
    queryset = Attendee.objects.all()
