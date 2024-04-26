from django.db import models

# Quay model to represent a quay at the port
class Quay(models.Model):
    name = models.CharField(max_length=100)
    quay_type = models.CharField(max_length=50)  # "Passenger", "Tanker", or "General"
    capacity = models.IntegerField()  # Maximum ships that can be accommodated
    length_m = models.FloatField()  # Quay length in meters
    draft_m = models.FloatField()  # Quay draft in meters
    tools = models.JSONField()  # List of tools (e.g., passenger transport, oil handling, cargo handling)

    def __str__(self):
        return self.name


# Ship model to represent a ship arriving at the port
class Ship(models.Model):
    name = models.CharField(max_length=100)
    ship_type = models.CharField(max_length=50)  # "Passenger", "Tanker", or "Cargo"
    size = models.IntegerField()  # Represents tonnage
    length_m = models.FloatField()  # Ship length in meters
    draft_m = models.FloatField()  # Ship draft in meters
    arrival_time = models.DateTimeField()  # Arrival time
    departure_time = models.DateTimeField()  # Departure time
    required_tools = models.JSONField()  # Tools required by the ship
    assigned_quay = models.ForeignKey(
        Quay, null=True, blank=True, on_delete=models.SET_NULL
    )  # Foreign key to Quay model
