from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)
    
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['username', 
                  'email', 
                  'password', 
                  'password_confirm', 
                  'first_name', 
                  'last_name',
                  'access_token',
                  'refresh_token',
                ]
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }
    
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate_email(self, value):
    
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def validate(self, attrs):
       
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
       
        validated_data.pop('password_confirm')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        refresh = RefreshToken.for_user(user)
        
        user.access_token = str(refresh.access_token)
        user.refresh_token = str(refresh)
        
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)
    user = serializers.DictField(read_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid username or password')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Most include username and password')       

class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField(read_only=True)        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
    confirm_password = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value
    
    def validate_new_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    

