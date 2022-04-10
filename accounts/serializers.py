from rest_framework import serializers
from accounts.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from api.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={
            'input_type': 'password',
        }, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match!")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'tc']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={
            'input_type': 'password',
        }, write_only=True)
    password2 = serializers.CharField(max_length=255, style={
            'input_type': 'password',
        }, write_only=True)
    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match!")
        user.set_password(password)
        user.save()
        return super().validate(attrs)

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            data = {
                'subject': 'Reset Your Password',
                'body': f'''To reset your password at JWTAuth enter the uid and token provided below:
uid:   {uid}
token: {token}

Warning: Do not share your reset password credentials i.e uid and token.
                ''',
                'to_email': user.email,
            }
            Util.send_mail(data)
            return attrs
        else:
            raise serializers.ValidationError('user is not registered')

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={
            'input_type': 'password',
        }, write_only=True)
    password2 = serializers.CharField(max_length=255, style={
            'input_type': 'password',
        }, write_only=True)
    
    class Meta:
        fields = ['password', 'password2']
    
    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm password doesn't match!")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("token may be expired or invalid!")
            user.set_password(password)
            user.save()
        except DjangoUnicodeDecodeError as identifer:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("token may be expired or invalid!")
        return super().validate(attrs)