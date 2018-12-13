import rest_auth.serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers

from pager.models import Device, Organization, Operation, OperationPropertyLocation, OperationKeywords, \
    OperationLoop

# Get the UserModel
UserModel = get_user_model()


class LoginSerializer(rest_auth.serializers.LoginSerializer):
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['username']
        return fields

    def validate(self, attrs):
        return super(LoginSerializer, self).validate(attrs)


class OperationPropertyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationPropertyLocation
        fields = '__all__'


class OperationKeywordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationKeywords
        fields = '__all__'


class OperationLoopSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationLoop
        exclude = ('operation',)


class OperationSerializer(serializers.ModelSerializer):
    einsatzort = OperationPropertyLocationSerializer(required=False)
    zielort = OperationPropertyLocationSerializer(required=False)

    keywords = OperationKeywordsSerializer(required=False)
    loops = OperationLoopSerializer(required=False, many=True)

    access_key = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = Operation
        exclude = ('organization', 'debug_response')

    def create(self, validated_data):
        einsatzort, zielort, keywords = None, None, None

        if 'einsatzort' in validated_data:
            einsatzort_data = validated_data.pop('einsatzort')
            einsatzort = OperationPropertyLocationSerializer.create(OperationPropertyLocationSerializer(),
                                                                    einsatzort_data)

        if 'zielort' in validated_data:
            zielort_data = validated_data.pop('zielort')
            zielort = OperationPropertyLocationSerializer.create(OperationPropertyLocationSerializer(), zielort_data)

        if 'keywords' in validated_data:
            keywords_data = validated_data.pop('keywords')
            keywords = OperationKeywordsSerializer.create(OperationKeywordsSerializer(), keywords_data)

        loops_data = validated_data.pop('loops')

        instance = Operation.objects.create(**validated_data)
        instance.einsatzort = einsatzort
        instance.zielort = zielort
        instance.keywords = keywords

        instance.save()

        for loop in loops_data:
            loop['operation'] = instance
            OperationLoopSerializer.create(OperationLoopSerializer(), loop)

        return instance


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ('owner',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        exclude = ('access_key', 'owner', 'push_title', 'push_message')
