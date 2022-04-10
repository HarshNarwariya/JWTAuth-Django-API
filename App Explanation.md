### Settings

```python
...

INSTALLED_APPS = [
  ...
  # developer apps
  'accounts.apps.AccountsConfig',
  'api.apps.ApiConfig',
  ...
  # 3rd party apps
  'corsheaders',
  'rest_framework',
  'rest_framework_simplejwt',
]

MIDDLEWARE = [
  ...
  # Middleware to allow cross origin
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware', 
  ...
]

# Time zone to IST
TIME_ZONE = 'Asia/Kolkata'

# Rest Framework auth class settings
# set to JWTAuthentication
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Settings of JWTAuthentication
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Which origins to allow
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# which model to be used for authntication
AUTH_USER_MODEL = 'accounts.User'

# Password reset timeout
PASSWORD_RESET_TIMEOUT = 600

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxx'

...
```

### AUTH Model
```python
import django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, tc, password=None, password2=None):
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            tc=tc,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tc, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            tc=tc,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
```

### Register auth model to admin site
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User

# Register your models here.
class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'tc', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tc')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email', 'id')
    filter_horizontal = ()

admin.site.register(User, UserModelAdmin)
```

### Serializing the Auth model
```python
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
```

### Renderer
```python
from rest_framework import renderers
import json

class UserRenderer(renderers.JSONRenderer):
    charset = 'UTF-8'
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'ErrorDetail' in str(data):
            response = json.dumps({
                'errors': data,
            })
        else:
            response = json.dumps(data)
        return response
```

### Send Email
```python
from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_mail(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email='iamyourbabyfortonight@gmail.com',
            to=[data['to_email']],
        )
        email.send(fail_silently=False)
```

### API views
```python
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from accounts.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer
from api.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

# Generate Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer,]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = get_tokens_for_user(user)
        return Response(data=data, status=status.HTTP_201_CREATED)
        

class UserLoginView(APIView):
    renderer_classes = [UserRenderer,]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            data = get_tokens_for_user(user)
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={
                'errors': {
                    'non_field_errors': [
                        'email or password is not valid',
                    ],
                },
            }, status=status.HTTP_404_NOT_FOUND)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer,]
    permission_classes = [IsAuthenticated,]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)   

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer,]
    permission_classes = [IsAuthenticated,]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data,
            context={
                'user': request.user,
            }   
        )
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': 'password changed successfully',
        }, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer,]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': 'password reset link sent successfully, please check your email.',
        }, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer,]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(
            data=request.data,
            context = {
                'uid': uid,
                'token': token,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response({
            'success': 'password reset successfully.',
        }, status=status.HTTP_200_OK)
```
