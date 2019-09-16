from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from django.views import View
from .models import Banks, Branches
from .serializers import BranchSerializer

# from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

class BankDetailsWithIFSC(APIView):
    permission_class = (IsAuthenticated, )
    def get(self, request, ifsc):
        limit = 0
        offset = 0
        try:
            limit = request.GET.get('limit', 0)
            limit = int(limit)
        except:
            limit = 0
        try:
            offset = request.GET.get('offset', 0)
            offset = int(offset)
        except:
            offset = 0

        ## I don'think offset and limit are required for this but as per the documentation I have added below limes for limit and offset
        # print("limit, offset:",limit, offset) 
        if limit or offset:
            branch = Branches.objects.filter(ifsc__iexact=ifsc)[offset:offset+limit]
            serializer = BranchSerializer(branch, many=True)
        else:
            branch = Branches.objects.filter(ifsc__iexact=ifsc).first()
            serializer = BranchSerializer(branch)
        return JsonResponse(serializer.data, safe=False)

class BankDetailsWithBranchCity(APIView):
    permission_class = (IsAuthenticated, )
    def get(self, request, bank, city):
        limit = 10
        offset = 0
        try:
            limit = request.GET.get('limit', 10)
            limit = int(limit)
        except:
            limit = 10
        try:
            offset = request.GET.get('offset', 0)
            offset = int(offset)
        except:
            offset = 0
        branch_qset = Branches.objects.filter( city__iexact=city, bank__name__icontains=bank)[offset:offset+limit]
        # branch_qset = Branches.objects.get(city__iexact=city, bank__name__icontains=bank)#[offset:offset+limit]
        # print("branch_qset:", branch_qset[offset:offset+limit])
        serializer = BranchSerializer(branch_qset, many=True)
        return JsonResponse(serializer.data, safe=False)
