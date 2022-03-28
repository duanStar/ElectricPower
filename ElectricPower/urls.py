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

    path('edata_year/', v4.edata_year),
    path('edata_predict/', v4.edata_predict),
    path('edata_every/', v4.edata_every),
    path('edata_category/', v4.edata_category),

    path('resume_lb1/', v4.res_summary_of_date),
    path('resume_lb2/', v4.res_middle_bottom_bar),
    path('resume_lb3/', v4.res_right_bottom_pie),
    path('resume_lb4/', v4.res_dynamic_time_series),
    path('resume_lb5/', v4.res_area_line),

]

urlpatterns += staticfiles_urlpatterns()
