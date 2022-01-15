from rest_framework import serializers
from .models import Bus, Location, Allocation
from django.contrib.auth.models import User



class AllocationSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Allocation
        fields = "__all__"


class BusSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Bus
        fields = "__all__"

class LocationSerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = Location
        fields = "__all__"




class LocationSerializer(serializers.ModelSerializer):  
    class Meta:
        model = Location
        fields = '__all__'


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'



# class Locationrerializer(serializers.ModelSerializer):  # create class to serializer user model
#     movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())

#     class Meta:
#         model = Location
#         fields = ('id', 'username', 'movies')