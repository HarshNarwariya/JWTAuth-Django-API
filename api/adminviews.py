from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from accounts.models import User
from api.paginator import StandardResultsSetPagination
from accounts.serializers import UserProfileSerializer

class UsersListView(ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminUser]
    pagination_class  = StandardResultsSetPagination
    serializer_class = UserProfileSerializer