
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/auth/login/$', obtain_jwt_token, name="api-login"),
    url(r'^bank_d/', include(('bank_d.urls', "bank-api"), namespace="bank-api")),
]
