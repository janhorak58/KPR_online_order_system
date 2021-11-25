"""todowoo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from order_system import views


from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    
    path('hledat/', views.searchOrder, name="searchOrder"),
    path('prehled/<int:m>/<int:y>/<str:zmena>/', views.prehled, name="prehled"),
    path('prehled/<int:m>/<int:y>/', views.prehled, name="prehled"),
    path('prehled/<int:m>/', views.prehled, name="prehled"),
    path('prehled/', views.prehled, name="prehled"),
    
    path('pridat/', views.addOrder, name="addOrder"),
    path('upravit/<int:pk>/', views.editOrder, name="editOrder"),
        
    path('odstranit/<int:pk>/', views.deleteOrder, name="deleteOrder"),
    path('detail/<int:pk>/', views.detailOrder, name="detailOrder"),
    path('pridatKnihu/<int:pk>/', views.addBook, name="addBook"),
    path('upravitKnihu/<int:pk>/<int:sk>/', views.editBook, name="editBook"),
    path('vymazatKnihu/<int:pk>/<int:sk>/', views.deleteBook, name="deleteBook"),
    
    
    
    path('loginuser/', views.loginuser, name="loginuser"),
    path('logoutuser/', views.logoutuser, name="logoutuser"),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) 
