from rest_framework import serializers
from .models import Banks, Branches

class BranchSerializer(serializers.ModelSerializer):
    bank = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Branches
        fields = (
                    'ifsc', 
                    'bank', 
                    'branch', 
                    'address',
                    'city', 
                    'district', 
                    'state'
                 )
   
