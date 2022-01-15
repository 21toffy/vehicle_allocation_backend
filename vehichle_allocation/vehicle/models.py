from django.db import models

CONSUMPTION_CHOICES = (
    ("low", "low"),
    ("fair", "fair"),
    ("high", "high"),
)
CONDITION_CHOICES = (
    ("bad", "bad"),
    ("fair", "fair"),
    ("good", "good"),
)

DISTANCE_CHOICES = (
    ("close", "close"),
    ("average", "average"),
    ("far", "far"),
)

class Bus(models.Model):
    name = models.CharField(max_length=100)
    engine = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    fuel_consumption = models.CharField(max_length=100, choices = CONSUMPTION_CHOICES, default = 'low')
    plate_number = models.CharField(max_length=100)
    seat_capacity = models.IntegerField()
    in_use = models.BooleanField(default=True)
    condition = models.CharField(max_length=100, choices = CONDITION_CHOICES, default = 'good')
    under_maintenance = models.BooleanField(default=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='bus_creator', on_delete=models.CASCADE)

    def __str__(self):
        return f'name: {self.name}  model: {self.model}, seat capacity: {self.seat_capacity}'
    class Meta:
        ordering = ['-id']


class Location(models.Model):
    destination = models.CharField(max_length=100)
    distance_in_km = models.IntegerField()
    distance_description =  models.CharField(max_length=100, choices = DISTANCE_CHOICES, default = 'close')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='location_creator', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.distance_in_km <= 150:
            self.distance_description = 'close'
            super(Location, self).save(*args, **kwargs)
        elif self.distance_in_km > 150 and self.distance_in_km <500:
            self.distance_description = 'average'
            super(Location, self).save(*args, **kwargs)
        elif self.distance_in_km >= 500:
            self.distance_description = 'far'
            super(Location, self).save(*args, **kwargs) 
        else:
            pass


    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.destination


class Allocation(models.Model):
    number_of_passengers = models.IntegerField()
    location = models.ForeignKey(Location, related_name='allocations', on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, related_name='allocations', on_delete=models.CASCADE)
    driver = models.CharField(max_length=100)
    date_of_journey = models.DateField()
    vehicle_condition = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey('auth.User', related_name='movies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.number_of_passengers + self.location + self.bus + self.driver + self.date_of_journey + self.vehicle_condition