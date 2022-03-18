"""ElectricPower URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from app import views as v4
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),    # 'root' + 'thereare2apples'
    path('', v4.index),


    path('login/', v4.login),
    path('register/', v4.register),

    path('mul_source/', v4.mul_source),
    path('eco_evolution/', v4.eco_evolution),
    path('dpm_warning/', v4.dpm_warning),
    path('lod_warning/', v4.lod_warning),
    path('res_analysis/', v4.res_analysis),



]

urlpatterns += staticfiles_urlpatterns()
