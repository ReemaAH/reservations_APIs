from rest_framework import serializers

from .models import CustomUser


class  UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'employee_number',
            'password',
            'first_name', 
            'last_name',
            'role'
        )
        extra_kwargs = {'employee_number': {'required': True, 'allow_blank': False}}
        extra_kwargs = {'password': {'required': True,'allow_blank': False}}
        extra_kwargs = {'first_name': {'required': True,'allow_blank': False}}
        extra_kwargs = {'last_name': {'required': True,'allow_blank': False}}
        extra_kwargs = {'role': {'required': True,'allow_blank': False}}

    def create(self, validated_data):
        auth_user = CustomUser.objects._create_user(**validated_data)
        return auth_user
