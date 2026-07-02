from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import Bounty
from .serializers import BountySerializer, UserRegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [AnonRateThrottle]


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class BountyListCreateView(generics.ListCreateAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        # Enforces isolation; users can only interact with their own query sets
        return Bounty.objects.filter(owner=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        # Clear cache on modification to protect freshness
        cache.delete(f"bounties_list_{self.request.user.id}")

    def list(self, request, *args, **kwargs):
        cache_key = f"bounties_list_{request.user.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
            
        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=120) # Cache limits set to 2 minutes
        return response


class BountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        # Eliminates data leakage leaks; returns a 404 instead of 403 on mismatched targets
        return Bounty.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f"bounties_list_{self.request.user.id}")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"bounties_list_{self.request.user.id}")
