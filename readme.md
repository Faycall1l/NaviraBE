# Port Simulation Project

This Django project simulates port operations, including ship assignments, quay management, and reassignment logic. It features a simulation module where you can adjust the speed to control the rate at which events occur.


# Endpoints

Below are some of the key endpoints for interacting with ships, quays, and the simulation:

```/api/list_quays/```: Lists all quays in the port.
```/api/find_suitable_quay/<int:ship_id>/```: Finds the most suitable quay for a given ship.
```/api/simulation/```: Starts the port simulation with adjustable speed control.