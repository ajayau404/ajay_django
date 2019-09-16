from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import BankDetailsWithIFSC, BankDetailsWithBranchCity

urlpatterns = {
    url(r'^ifsc/(?P<ifsc>[A-Za-z]{4}\w{7})$', BankDetailsWithIFSC.as_view(), name="get-ifsc"),
    url(r'^branches/(?P<bank>.*)/(?P<city>.*)$', BankDetailsWithBranchCity.as_view(), name="get-branch")

}

urlpatterns = format_suffix_patterns(urlpatterns)