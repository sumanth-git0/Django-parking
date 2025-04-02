from .models import parkhistory, parkspace, parkuser
from rest_framework import serializers


class parkspaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = parkspace
        fields = ['Level', 'TWA', 'FWA']


class parkhistorySerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = parkhistory
        fields = ['Level', 'Type', 'VehicleNumber', 'Lot', 'Intime', 'Outtime', 'Fee']