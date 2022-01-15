from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from  django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

import datetime

def exception_handler(exception):
    template = "An exception of type {0} occurred. Arguments:{1!r}"
    message = template.format(type(exception).__name__, exception.args)
    return message


class ListBus(APIView):
    def get(request, *args, **kwargs):
        if kwargs['condition'] not in ['all', 'good', 'bad', 'fair', 'under_maintenace', 'in_use']:
            return Response({"data":[], 'message':"Wrong data passed"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if kwargs['condition'] == 'all':
                busses = Bus.objects.all()
                serializer = BusSerializer(busses, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif kwargs['condition'] in ['good', 'bad', 'fair']:
                busses = Bus.objects.filter(condition = kwargs['condition'])
                serializer = BusSerializer(busses, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            elif kwargs['condition'] == 'under_maintenace':
                busses = Bus.objects.filter(under_maintenance = True)
                serializer = BusSerializer(busses, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif kwargs['condition'] == 'in_use':
                busses = Bus.objects.filter(in_use = True)
                serializer = BusSerializer(busses, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"data":[], 'message':"Wrong data passed"}, status=status.HTTP_400_BAD_REQUEST)



class ListLocation(APIView):
    def get(request, *args, **kwargs):
        locations = Location.objects.filter(distance_description = kwargs['distance'])
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
       




class BusView(APIView):
    # def get(self,request):
    #     books = models.Books.objects.all()
    #     res = BookAll(instance=books,many=True)
    #     return JsonResponse(res.data,safe=False)
 
    def post(self,request):
        try:
            data = request.data
            user = User.objects.filter(pk=1).first()
            print(user)
            bus = Bus.objects.create(
                name=data.get('name'),
                engine=data.get('engine'),
                model=data.get('model'),
                fuel_consumption=data.get('fuel_consumption'),
                plate_number=data.get('plate_number'),
                seat_capacity=data.get('seat_capacity'),
                in_use=data.get('in_use'),
                condition=data.get('condition'),
                under_maintenance=data.get('under_maintenance'),
                year=data.get('year'),
                # creator=self.request.user,
                creator = user
                )
            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = exception_handler(e)
            return Response({"data":[], 'message':response}, status=status.HTTP_400_BAD_REQUEST)
 
 
    def patch(self, request, *args, **kwargs):
        bus = get_object_or_404(Bus, pk=kwargs['bus_id'])
        serializer = BusSerializer(bus, data=request.data, partial=True)
        if serializer.is_valid():
            bus = serializer.save()
            return Response(BusSerializer(bus).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
    def delete(self,request, *args, **kwargs):
        data = request.data
        try:
            Bus.objects.filter(id=kwargs['bus_id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except Bus.DoesNotExist:
            return Response({"data":[], 'message':"bus does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class LocationView(APIView):
    # def get(self,request):
    #     books = models.Books.objects.all()
    #     res = BookAll(instance=books,many=True)
    #     return JsonResponse(res.data,safe=False)
 
    def post(self,request):
        try:
            data = request.data
            user = User.objects.filter(pk=1).first()
            print(user)
            location = Location.objects.create(
                destination=data.get('destination'),
                distance_in_km=data.get('distance_in_km'),
                distance_description=data.get('distance_description'),

                # creator=self.request.user,
                creator = user
                )
            created_location = Location.objects.get(id=location.id)
            print(created_location)
            return Response(request.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = exception_handler(e)
            return Response({"data":[], 'message':response}, status=status.HTTP_400_BAD_REQUEST)
 


    def patch(self, request, *args, **kwargs):
        location = get_object_or_404(Location, id=kwargs['location_id'])
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            location = serializer.save()
            return Response(LocationSerializer(location).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, *args, **kwargs):
        data = request.data
        try:
            Location.objects.filter(id=kwargs['bus_id']).first().delete()
            return Response(status=status.HTTP_200_OK)
        except Location.DoesNotExist:
            return Response({"data":[], 'message':"location does not exist"}, status=status.HTTP_400_BAD_REQUEST)




class ListSuitableBussesView(APIView):
    def get(request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        location=data.get('location')
        passangers=data.get('passangers')
        location_status = Location.objects.filter(destination__icontains = location).first()

        try:
            if location_status.distance_description=="far":
                bus = Bus.objects.filter(fuel_consumption = 'low', 
                                        condition = "good", in_use=False, 
                                        under_maintenance = False, 
                                        seat_capacity__gte=passangers)
                serializer = BusSerializer(bus, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


            elif location_status.distance_description == "average":
                bus = Bus.objects.filter(Q(fuel_consumption = 'low') | Q(fuel_consumption = 'fair'),
                                        Q(condition = "good") | Q(condition = "fair"),
                                        in_use=False,
                                        under_maintenance = False,
                                        seat_capacity__gte=passangers)
                serializer = BusSerializer(bus, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


            elif location_status.distance_description == "close":
                bus = Bus.objects.filter(fuel_consumption = 'high', 
                                        condition = "fair", 
                                        in_use=False, 
                                        under_maintenance = False, 
                                        seat_capacity__gte=passangers)
                serializer = BusSerializer(bus, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)


            else:
                bus = Bus.objects.filter(in_use=False, under_maintenance = False, )
                serializer = BusSerializer(bus, many=True)


                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"data":[], 'message':f"bus probablt does not exist in DB/ {e}"}, status=status.HTTP_400_BAD_REQUEST)

       

class AllocateBusView(APIView):

    def post(self,request):
        try:
            data = request.data
            user = User.objects.filter(pk=1).first()
            print(user)
            # date_of_journey = datetime.datetime.strptime(date, "%Y-%m-%d")
            location = Location.objects.filter(destination__icontains = data.get('location')).first()
            bus = Bus.objects.get(id = data.get('bus'))

            print(location)
            allocation = Allocation.objects.create(
                number_of_passengers=data.get('number_of_passengers'),
                location=location,
                bus=bus,
                driver=data.get('driver'),
                date_of_journey = data.get('date_of_journey'),
                vehicle_condition=data.get('vehicle_condition'),   
                creator = user
                )
            print(bus.in_use)
            # atering_bus_in_use = 
            bus.in_use = True
            bus.save()
            print(bus.in_use)
            print(bus.id)

            
            return Response({"data":request.data, 'message':"Vehicle allocated successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = exception_handler(e)
            return Response({"data":[], 'message':response}, status=status.HTTP_400_BAD_REQUEST)
 