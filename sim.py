import datetime
import random
import time

class Quay:
    def __init__(self, name, quay_type, capacity, length_m, draft_m, tools):
        self.name = name
        self.quay_type = quay_type  # "Passenger", "Tanker", or "General"
        self.capacity = capacity  
        self.length_m = length_m  
        self.draft_m = draft_m  
        self.tools = tools  # Tools available at the quay (e.g., passenger transport, oil handling, cargo handling)
        self.occupied_by = [] 

    def is_free(self):
        return len(self.occupied_by) < self.capacity

    def can_accommodate(self, ship):
        has_correct_dimensions = self.length_m >= ship.length_m and self.draft_m >= ship.draft_m
        has_required_tools = all(tool in self.tools for tool in ship.required_tools)
        return has_correct_dimensions and has_required_tools

    def assign_ship(self, ship):
        if self.can_accommodate(ship) and self.is_free():
            self.occupied_by.append(ship)
            ship.assigned_quay = self
            return True
        return False

    def remove_ship(self, ship):
        if ship in self.occupied_by:
            self.occupied_by.remove(ship)


class Ship:
    def __init__(self, name, ship_type, size, length_m, draft_m, arrival_time, departure_time, required_tools):
        self.name = name
        self.ship_type = ship_type 
        self.size = size 
        self.length_m = length_m
        self.draft_m = draft_m 
        self.arrival_time = arrival_time
        self.departure_time = arrival_time + datetime.timedelta(hours=random.randint(4, 12))
        self.required_tools = required_tools 
        self.assigned_quay = None
    
    def get_details(self):
        return (
            f"Ship {self.name}:\n"
            f"  Type: {self.ship_type}\n"
            f"  Size: {self.size} tons\n"
            f"  Length: {self.length_m}m\n"
            f"  Draft: {self.draft_m}m\n"
            f"  Arrival Time: {self.arrival_time}\n"
            f"  Departure Time: {self.departure_time}\n"
            f"  Required Tools: {', '.join(self.required_tools)}\n"
        )



class PortScheduler:
    def __init__(self, quays):
        self.quays = quays 

    def find_suitable_quays(self, ship):
        suitable_quays = [
            quay for quay in self.quays if quay.can_accommodate(ship) and quay.is_free()
        ]

        return suitable_quays

    def reassign_cargo_from_priority_quays(self):
        cargo_in_priority_quays = [
            ship
            for quay in self.quays
            if quay.quay_type in ["Passenger", "Tanker"]
            for ship in quay.occupied_by
            if ship.ship_type == "Cargo"
        ]

        for cargo_ship in cargo_in_priority_quays:
            suitable_quays = [
                quay for quay in self.quays if quay.quay_type == "General" and quay.is_free()
            ]
            if suitable_quays:
                best_quay = suitable_quays[0]
                for current_quay in self.quays:
                    if cargo_ship in current_quay.occupied_by:
                        current_quay.remove_ship(cargo_ship)
                        break
                best_quay.assign_ship(cargo_ship)
                print(f"Reassigned {cargo_ship.name} to {best_quay.name}")

quays = [
    Quay("Passenger Quay", "Passenger", 1, 200, 10, ["passenger transport", "cargo handling"]),
    Quay("Tanker Quay 1", "Tanker", 1, 150, 12, ["oil handling", "cargo handling"]),
    Quay("Tanker Quay 2", "Tanker", 1, 150, 12, ["oil handling", "cargo handling"]),
    Quay("Tanker Quay 3", "Tanker", 1, 150, 12, ["oil handling", "cargo handling"]),
    Quay("Tanker Quay 4", "Tanker", 1, 150, 12, ["oil handling", "cargo handling"]),
    *[Quay(f"General Quay {i}", "General", 1, 180, 9, ["cargo handling"]) for i in range(1, 22)]
]

scheduler = PortScheduler(quays)


pre_assigned_ships = [
    Ship("Pre-assigned Passenger 1", "Passenger", 10000, 150, 8, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=6), ["passenger transport"]),
    Ship("Pre-assigned Tanker 1", "Tanker", 15000, 140, 11, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=7), ["oil handling"]),
    Ship("Pre-assigned Cargo 1", "Cargo", 12000, 160, 9, datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(hours=5), ["cargo handling"]),
]

quays[0].assign_ship(pre_assigned_ships[0])
quays[1].assign_ship(pre_assigned_ships[1])  
quays[6].assign_ship(pre_assigned_ships[2])  


for quay in quays:
    if quay.occupied_by:
        print(f"{quay.name} is occupied by:")
        for ship in quay.occupied_by:
            print(f"  - {ship.name}")

simulation_duration = 120 
ship_arrival_interval = 10

ships = []


for i in range(simulation_duration // ship_arrival_interval):
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

    arrival_time = datetime.datetime.now() + datetime.timedelta(seconds=i * ship_arrival_interval)
    departure_time = arrival_time + datetime.timedelta(hours=random.randint(4, 12))

    ship = Ship(
        ship_name,
        ship_type,
        ship_size,
        ship_length,
        ship_draft,
        arrival_time,
        departure_time,
        required_tools[ship_type],
    )

    ships.append(ship)


for ship in ships:
    print(ship.get_details())


simulation_start = datetime.datetime.now()
simulation_end = simulation_start + datetime.timedelta(seconds=simulation_duration)

while datetime.datetime.now() < simulation_end:
    for ship in ships:
        if ship.arrival_time <= datetime.datetime.now() and not ship.assigned_quay:
            suitable_quays = scheduler.find_suitable_quays(ship)
            if ship.ship_type == "Cargo":
                suitable_quays = [q for q in suitable_quays if q.quay_type == "General"] or suitable_quays
            if suitable_quays:
                best_quay = suitable_quays[0]
                best_quay.assign_ship(ship)
                print(f"{ship.name} assigned to {suitable_quays[0].name}")

    time.sleep(10) 

    for quay in scheduler.quays:
        for ship in quay.occupied_by[:]:
            if ship.departure_time <= datetime.datetime.now():
                quay.remove_ship(ship)
                print(f"{ship.name} left {quay.name}")

    scheduler.reassign_cargo_from_priority_quays()
