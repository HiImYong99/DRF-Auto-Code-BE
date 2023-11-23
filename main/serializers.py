
from rest_framework import serializers
from .models import UserInput, AIOutput


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInput
        fields = ['language', 'purpose', 'detail']


class AIOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIOutput
        fields = ['answer']
