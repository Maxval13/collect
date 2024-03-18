from django.contrib.auth.models import Group, User
from rest_framework import serializers
from payment.models import Attendee, Account, Action, Payment, Collect, Reason


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'balance')
        read_only_fields = ('id', 'balance')

class ReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reason
        fields = ('id', 'name')

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendee
        fields = ('id', 'first_name', 'last_name', 'image')
        read_only_fields = ('id',)

    def create(self, validated_data):

        validated_data['user_id'] = self.context['request'].user.id
        return super(AttendeeSerializer, self).create(validated_data)


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'account', 'amount', 'date')
        read_only_fields = ('id', 'date')

    def create(self, validated_data):
        if validated_data['account'].balance + validated_data['amount'] > 0:
            validated_data['account'].balance += validated_data['amount']
            validated_data['account'].save()
        else:
            raise serializers.ValidationError('Not enough money')

        return super(ActionSerializer, self).create(validated_data)


class PaymentSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(TransferSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            self.fields['from_account'].queryset = self.fields['from_account']\
                .queryset.filter(user=self.context['view'].request.user)

    to_account = serializers.CharField()

    def validate(self, data):
        try:
            data['to_account'] = Account.objects.get(pk=data['to_account'])
        except Exception as e:
            print(e)
            raise serializers.ValidationError(
                "No such account from serializer")
        return data

    class Meta:
        model = Payment
        fields = ('id', 'from_account', 'to_account', 'amount', 'datetime_pay')
        read_only_fields = ('id', )


class CollectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collect
        fields = ('id', 'author_collection', 'name_collection', 'reason', 'content', 'amount_full', 'amount_now',
                  'count', 'image', 'deadline_date')
        read_only_fields = ('id',)
