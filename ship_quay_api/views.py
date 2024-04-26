from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import random
from .models import Quay, Ship

# Example view to get a list of quays based on ships
def list_quays(request):
    # Create random ships for demonstration
    ships = []
    for i in range(10):  # Generate 10 random ships
        ship_name = f"Random Ship {random.randint(1, 1000)}"
        ship_type = random.choice(["Passenger", "Tanker", "Cargo"])
        ship_size = random.randint(5000, 20000)
        ship_length = random.randint(120, 200)
        ship_draft = random.uniform(5.0, 12.0)

        # Determine required tools based on ship type
        required_tools = {
            "Passenger": ["passenger transport", "cargo handling"],
            "Tanker": ["oil handling", "cargo handling"],
            "Cargo": ["cargo handling"]
        }

        arrival_time = datetime.now()
        departure_time = arrival_time + timedelta(hours=random.randint(4, 12))

        ship = Ship(
            name=ship_name,
            ship_type=ship_type,
            size=ship_size,
            length_m=ship_length,
            draft_m=ship_draft,
            arrival_time=arrival_time,
            departure_time=departure_time,
            required_tools=required_tools[ship_type],
        )
        ships.append(ship)

    # Find suitable quays for each ship without 'contains' lookup
    suitable_quays = []
    quays = Quay.objects.all()

    for ship in ships:
        for quay in quays:
            # Check if the quay meets ship requirements
            if (
                quay.capacity > 0  # Quay has capacity
                and quay.length_m >= ship.length_m  # Length is sufficient
                and quay.draft_m >= ship.draft_m  # Draft is sufficient
                and set(ship.required_tools).issubset(set(quay.tools))  # Required tools are available
            ):
                suitable_quays.append(quay)
                break  # Exit loop once suitable quay is found

    # Return the suitable quays as a JSON response
    quay_list = [{"name": q.name, "type": q.quay_type, "capacity": q.capacity} for q in suitable_quays]
    return JsonResponse({"quays": quay_list})
