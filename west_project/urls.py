from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.split('/')), # Optional admin panel access
    path('api/', include('bounties.urls')),
]
