from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
import random
from .models import Quay, Ship
from django.shortcuts import get_object_or_404
from django.core import serializers


def list_quays(request):

    ships = []
    for i in range(10):  # Generate 10 random ships
        ship_name = f"Random Ship {random.randint(1, 1000)}"
        ship_type = random.choice(["Passenger", "Tanker", "Cargo"])
        ship_size = random.randint(5000, 20000)
        ship_length = random.randint(120, 200)
        ship_draft = random.uniform(5.0, 12.0)

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

    suitable_quays = []
    quays = Quay.objects.all()

    for ship in ships:
        for quay in quays:
            if (
                quay.capacity > 0  
                and quay.length_m >= ship.length_m  
                and quay.draft_m >= ship.draft_m
                and set(ship.required_tools).issubset(set(quay.tools))  
            ):
                suitable_quays.append(quay)
                break 

    quay_list = [{"name": q.name, "type": q.quay_type, "capacity": q.capacity} for q in suitable_quays]
    return JsonResponse({"quays": quay_list})


def find_suitable_quay(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)

    quays = Quay.objects.all()

    if ship.ship_type == "Cargo":
        suitable_quays = [
            quay for quay in quays
            if quay.quay_type == "General"
            and quay.is_free()
            and quay.length_m >= ship.length_m
            and quay.draft_m >= ship.draft_m
        ]
        if not suitable_quays:
            suitable_quays = [
                quay for quay in quays
                if quay.is_free()
                and quay.length_m >= ship.length_m
                and quay.draft_m >= ship.draft_m
            ]
    else:
        if ship.ship_type in ["Passenger", "Tanker"]:
            for quay in quays:
                if quay.quay_type in ["Passenger", "Tanker"]:
                    cargo_to_reassign = [
                        cargo for cargo in quay.ships.all()
                        if cargo.ship_type == "Cargo"
                    ]
                    for cargo in cargo_to_reassign:
                        general_quay = next(
                            (q for q in quays if q.quay_type == "General" and q.is_free()),
                            None
                        )
                        if general_quay:
                            cargo.quay = general_quay
                            cargo.save()
###
#                        if not suitable_quays:  # Reassign cargo ships to free up a quay
#                for quay in quays:
#                    if quay.quay_type in ["Passenger", "Tanker"]:
#                        cargo_to_reassign = [
#                            cargo for cargo in quay.ships.all()
#                            if cargo.ship_type == "Cargo"
#                        ]
#                        for cargo in cargo_to_reassign:
#                            general_quay = next(
#                                (q for q in quays if q.quay_type == "General" and q.is_free()),
#                                None
#                            )
#                            if general_quay:
#                                # Reassign the cargo ship to a general quay
#                                cargo.quay = general_quay
#                                cargo.save()
#
#                # Retry finding a suitable quay after reassignment
#                suitable_quays = [
#                    quay for quay in quays
#                    if quay.quay_type == ship.ship_type
#                    and quay.is_free()
#                    and quay.length_m >= ship.length_m
#                    and quay.draft_m >= ship.draft_m
#               ]
###

        suitable_quays = [
            quay for quay in quays
            if quay.quay_type == ship.ship_type
            and quay.is_free()
            and quay.length_m >= ship.length_m
            and quay.draft_m >= ship.draft_m
        ]

    if suitable_quays:
        best_quay = suitable_quays[0]
        best_quay.ships.add(ship) 
        best_quay.save()

        quay_info = {
            "quay_name": best_quay.name,
            "quay_type": best_quay.quay_type,
            "length_m": best_quay.length_m,
            "draft_m": best_quay.draft_m,
            "tools": best_quay.tools,
        }
        return JsonResponse({"suitable_quay": quay_info})
    else:
        return JsonResponse({"error": "No suitable quay found."}, status=404)

def get_ship_details(request, ship_id):
    ship = get_object_or_404(Ship, id=ship_id)


    ship_data = {
        "id": ship.id,
        "name": ship.name,
        "type": ship.ship_type,
        "size": ship.size,
        "length": ship.length_m,
        "draft": ship.draft_m,
        "arrival_time": ship.arrival_time,
        "departure_time": ship.departure_time,
        "required_tools": ship.required_tools,
    }

    return JsonResponse({"ship_details": ship_data})