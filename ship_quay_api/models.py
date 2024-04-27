from django.db import models


class Ship(models.Model):
    name = models.CharField(max_length=100)
    length_m = models.FloatField()
    draft_m = models.FloatField()
    ship_type = models.CharField(max_length=50)
    quay = models.ForeignKey('Quay', related_name='ships', on_delete=models.SET_NULL, null=True, blank=True)


class Quay(models.Model):
    name = models.CharField(max_length=100)
    length_m = models.FloatField()  
    draft_m = models.FloatField()   
    quay_type = models.CharField(max_length=50) 
    capacity = models.IntegerField(default=0)
    tools = models.TextField(blank=True)

    def is_free(self):
        return self.ships.count() < self.capacity
