from django.db import models

# Ship model
class Ship(models.Model):
    name = models.CharField(max_length=100)
    length_m = models.FloatField()
    draft_m = models.FloatField()
    ship_type = models.CharField(max_length=50)
    quay = models.ForeignKey('Quay', related_name='ships', on_delete=models.SET_NULL, null=True, blank=True)

# Quay model
class Quay(models.Model):
    name = models.CharField(max_length=100)
    length_m = models.FloatField()  # Quay length
    draft_m = models.FloatField()   # Quay draft
    quay_type = models.CharField(max_length=50)  # e.g., Cargo, Passenger, etc.
    capacity = models.IntegerField(default=0)
    tools = models.TextField(blank=True)

    def is_free(self):
        return self.ships.count() < self.capacity
