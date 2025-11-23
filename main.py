"""
Created on Fri Nov 21 14:29:39 2025

@author: adyaakhera
"""

import random #will be used to introduce random obstacles
import matplotlib.pyplot as plt

#planet data dictionary contains all the information about planets in our database

# planetData contains all planet environments.
# grid_size = simulated area
# obstacles = known hazards
# planet_time = local hour (0–23)
# terrain_difficulty = movement cost
# sunlight_hours = (sunrise, sunset)

LOG_FILE = "mission_log.txt" #this will contain all the logs for this mission

def log_event(event_str):
    #we will log an event
    with open(LOG_FILE, "a") as f:
        f.write(event_str + "\n")
    print(event_str)  # printing the event to terminal as well 

planetData = {
    
    "Mars": {
        "name": "Mars",
        "terrain_type": "rocky",
        "grid_size": (10, 10),
        "obstacles": [(2,3), (5,5)],
        "resources": {"water_ice": 5, "minerals": 10},
        "battery_level": 100,
        "planet_time": 0,
        "color": "red",
        "terrain_difficulty": 2,
        "sunlight_hours": (6, 18)    
    },
    "Moon": {
        "name": "Moon",
        "terrain_type": "cratered",
        "grid_size": (12, 12),
        "obstacles": [(6,6), (8,8)],
        "resources": {"water_ice": 1, "minerals": 15},
        "battery_level": 100,
        "planet_time": 0,
        "color": "gray",
        "terrain_difficulty": 3,
        "sunlight_hours": (8, 20)     
    },
    "Jupiter": {
        "name": "Jupiter",
        "terrain_type": "gas",
        "grid_size": (15, 15),
        "obstacles": [(3,4), (10,12), (7,7)],
        "resources": {"hydrogen": 20, "helium": 15},
        "battery_level": 150,
        "planet_time": 0,
        "color": "orange",
        "terrain_difficulty": 1,
        "sunlight_hours": (5, 17)   
    },
    "Venus": {
        "name": "Venus",
        "terrain_type": "volcanic",
        "grid_size": (8, 8),
        "obstacles": [(1,2), (4,4), (6,1)],
        "resources": {"sulfur": 10, "minerals": 8},
        "battery_level": 80,
        "planet_time": 0,
        "color": "yellow",
        "terrain_difficulty": 3,
        "sunlight_hours": (10, 16)    
    },
    "Mercury": {
        "name": "Mercury",
        "terrain_type": "cratered",
        "grid_size": (6, 6),
        "obstacles": [(0,1), (3,3)],
        "resources": {"iron": 12, "minerals": 5},
        "battery_level": 70,
        "planet_time": 0,
        "color": "darkgray",
        "terrain_difficulty": 2,
        "sunlight_hours": (7, 19)   
    }
}

class Spacecraft():
    
    def __init__(self, name, position = (0,0), battery = 100): 
        #we give the spacecraft a default position of 0,0 and a default battery of 100
        self.name = name
        self.position = position
        self.battery = battery
        
    def calculate_new_position(self, direction):
        
        x, y = self.position

        dir_map = {
            "N": (0, 1),
            "S": (0, -1),
            "E": (1, 0),
            "W": (-1, 0)
        }

        if direction not in dir_map:
            return None

        dx, dy = dir_map[direction]
        
        return (x + dx, y + dy) #returning the updated position tuple
        
    def moveRover(self, direction, planet):
        #we will use the battery to move the rover in the NSEW directions
        #we will consider 1 unit on this scale to be about 1 km
        
        new_pos = self.calculate_new_position(direction)
        if (new_pos is None):
            log_event(f"{self.name}: invalid direction {direction}")
            return False

        x, y = new_pos
            
        #checking battery
        if self.battery <= 0:
            log_event(f"{self.name} cannot move. Battery depleted.")
            return False
        
        #checking planet gride size
        max_x, max_y = planet["grid_size"]
        if not (0 <= x < max_x and 0 <= y < max_y): #if the position is not within the grid, we print error
           log_event(f"{self.name} cannot move. Out of bounds at {new_pos}")
           return False
       
        if ((x,y) in planet["obstacles"]):
            log_event(f"{self.name} blocked by obstacle at {new_pos}")
            return False
        
        self.position = (x, y) #assigning the updated position to the rover
        self.battery -= 1 * planet["terrain_difficulty"] #consuming battery according to movement and terrain difficulty
        self.battery = max(self.battery, 0) #avoids battery from going negative
        log_event(f"{self.name} moved {direction} to {self.position}. Battery left: {self.battery:.1f}")
        return True
    
class Rover(Spacecraft):
    
    def __init__(self, name, position = (0,0), battery = 100, instruments = None):
        super().__init__(name, position, battery)
        # if the rover is assigned any instruments, they get added to the rover else it is an empty list
        #the instruments parameter will be a list
        if (instruments):
            self.instruments = instruments
        else:
            self.instruments = []
            
class ExperimentRover(Rover):
    def __init__(self, name, position = (0,0), battery = 100, instruments = None):
        super().__init__(name, position, battery, instruments)
        self.experiment_data = [] #creating empty list to store experiment data

    def perform_experiment(self, planet):
        if not self.instruments:
            log_event(f"{self.name} has no instruments")
            return
        instrument = random.choice(self.instruments)
        result = f"{instrument} measurement: {random.randint(1,100)}" #simulating an experiment reading
        self.experiment_data.append((planet["name"], self.position, result)) #storing the data as a tuple in the experiment data list
        log_event(f"{self.name} performed an experiment at {self.position} on {planet['name']}: {result}")

class Drone(Spacecraft):
    def __init__(self, name, position=(0, 0), battery=100, altitude=0, max_altitude=100):
        super().__init__(name, position, battery)
        self.altitude = altitude
        self.max_altitude = max_altitude

    def moveDrone(self, direction, planet):
        new_pos = self.calculate_new_position(direction)
        
        if (new_pos is None):
            log_event(f"{self.name}: invalid direction {direction}")
            return False
    
        x, y = new_pos
            
        #checking grid bounds
        max_x, max_y = planet["grid_size"]
        if not (0 <= x < max_x and 0 <= y < max_y):
            log_event(f"{self.name} out of bounds at {new_pos}")
            return False
        
        battery_usage = 2 #minimum battery usage required per movement

        if (self.battery < battery_usage) :
            log_event(f"{self.name} does not have enough battery to fly")
            return False

        #position and batter update
        self.position = (x, y)
        self.battery -= battery_usage #we don't need to use terrain difficulty as the drone is flying

        log_event(f"{self.name} flew {direction} to {self.position} at altitude {self.altitude}. Battery: {self.battery:.1f}")
        return True
    
    def changeAltitude(self, height):
        new_alt = self.altitude + height

        if (new_alt < 0):
            print(f"{self.name} cannot go below ground level.")
            return False
        
        if (new_alt > self.max_altitude):
            print(f"{self.name} cannot exceed a max altitude of {self.max_altitude}.")
            return False
        
        if (height > 5): #more battery usage for higher altitudes
            battery_usage = 3
        else:
            battery_usage = 1

        if (self.battery < battery_usage):
            print(f"{self.name} does not have sufficient battery to change altitude.")
            return False
        
        #updating altitude and battery
        self.altitude = new_alt
        self.battery -= battery_usage

        print(f"{self.name} changed altitude to {self.altitude}. Battery: {self.battery}")
        return True

def add_obstacles(planet, obs = 2):
    #this function will generate random obstacles and add it to a planet's known data
    max_x, max_y = planet["grid_size"]
    for i in range(obs):
        x, y = random.randint(0, max_x-1), random.randint(0, max_y-1) #generating obstacles at a random location
        if (x,y) not in planet["obstacles"]:
            planet["obstacles"].append((x,y))

def recharge(rover, planet):
    #this function will user solar power to recharge the rover during daytime
    sunlight_start, sunlight_end = planet["sunlight_hours"]
    if (sunlight_start <= planet["planet_time"] <= sunlight_end):
        rover.battery += 2 
        rover.battery = min(rover.battery, 100) #this will ensure battery doesn't go above 100
        print(f"{rover.name} is recharging. Battery: {rover.battery}")

class Mission(): #creating a mission
    def __init__(self, planet):
        self.planet = planet
        self.vehicles = [] #keeping a record of all the rovers or drones on that planet
        self.time = 1 #updates every hour

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)
        print(f"{vehicle.name} added to mission on {self.planet['name']}")

    def update_time(self, hours):
        self.time_step = hours
        self.planet["planet_time"] = (self.planet["planet_time"] + self.time_step) % 24 #staying within 24 hours earth time
        log_event(f"Time on {self.planet['name']} is now {self.planet['planet_time']}h")
        #we are not keeping track of days

    def recharge_all(self):
        for vehicle in self.vehicles:
            recharge(vehicle, self.planet)
    
    def random_obs(self, chance=0.3):
        if (random.random() < chance): #geenrating a number between 0 and 1 and using probability to generate obstacles
            add_obstacles(self.planet, obs=1)
            print("Unknown obstacle detected") #adding it to known obstacles

    def step(self): #one step of a rover
        self.update_time()
        self.recharge_all()
        self.random_obs()

    def status_report(self):
        print("\n=== Mission Status Report ===")
        print(f"Planet: {self.planet['name']}")
        print(f"Time: {self.planet['planet_time']}h")
        print(f"Known obstacles: {self.planet['obstacles']}")
        print("\nVehicles:")
        for v in self.vehicles:
            print(f"  - {v.name}: position={v.position}, battery={v.battery}")
        print("=============================\n")

# --- Example Mission Simulation ---

mars = planetData["Mars"]

mission = Mission(mars)

log_event(f"Planet: {mission.planet['name']}")
log_event(f"Time: {mission.planet['planet_time']}h")

r1 = Rover("Pathfinder", instruments=["camera"])
d1 = Drone("SkyScout", battery=120)

mission.add_vehicle(r1)
mission.add_vehicle(d1)

r1.moveRover("N", mars)
d1.moveDrone("E", mars)

mission.update_time(3)
mission.status_report()