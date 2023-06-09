from rest_framework import serializers
from .models import ApplicantCredit

class ApplicantCreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantCredit
        fields = ['name', 'lastname', 'dni', 'gender', 'email', 'mount', 'status']
        extra_kwargs = {'dni': {'required': True},
                        'name': {'required': True},
                        'lastname': {'required': True},
                        'mount': {'required': True},
                        'email': {'required': True}
                        }