"""
URL configuration for furniture project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework.routers import DefaultRouter


from users.views import *
from categories.views import CategoryViewSet
from products.views import ProductViewSet,ProductImageViewSet,MaterialViewSet


router = DefaultRouter()


router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'materials', MaterialViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    
    
    # __________________________ Authentication Endpoints _________________________________#

path(
        "auth/login",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "auth/logout",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "auth/refresh-token",
        RefreshTokenView.as_view(),
        name="refresh_token",
    ),
    path(
        "auth/change-password",
        ChangePasswordView.as_view(),
        name="change_password",
    ),
    # __________________________ Categories Endpoints _________________________________#

    path('', include(router.urls)),
    
    # __________________________ Products Endpoints _________________________________#

    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += debug_toolbar_urls()