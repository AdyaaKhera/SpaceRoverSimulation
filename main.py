#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 21 14:29:39 2025

@author: adyaakhera
"""

import random #will be used to introduce random obstacles
import matplotlib.pyplot as plt

#planet data dictionary contains all the information about planets in our database
planetData = {
    
    """
    grid size is the simulated area, 
    obstacles is the known obstacles coordinates, 
    planet_time is the current time
    terrain difficulty tell how hard it is to explore the terrain
    """
    
    "Mars": {
        "terrain_type": "rocky",
        "grid_size": (10, 10),
        "obstacles": [(2,3), (5,5)],
        "resources": {"water_ice": 5, "minerals": 10},
        "battery_level": 100,   
        "planet_time": 0,       
        "color": "red",
        "terrain_difficulty": 1.2  
    },
    "Moon": {
        "terrain_type": "cratered",
        "grid_size": (12, 12),
        "obstacles": [(6,6), (8,8)],
        "resources": {"water_ice": 1, "minerals": 15},
        "battery_level": 100,
        "planet_time": 0,
        "color": "gray",
        "terrain_difficulty": 1.5
    },
    "Jupiter": {
        "terrain_type": "gas",
        "grid_size": (15, 15),
        "obstacles": [(3,4), (10,12), (7,7)],
        "resources": {"hydrogen": 20, "helium": 15},
        "battery_level": 50,
        "planet_time": 0,
        "color": "orange",
        "terrain_difficulty": 1.0  
    },
    "Venus": {
        "terrain_type": "volcanic",
        "grid_size": (8, 8),
        "obstacles": [(1,2), (4,4), (6,1)],
        "resources": {"sulfur": 10, "minerals": 8},
        "battery_level": 80,
        "planet_time": 0,
        "color": "yellow",
        "terrain_difficulty": 1.4
    },
    "Mercury": {
        "terrain_type": "cratered",
        "grid_size": (6, 6),
        "obstacles": [(0,1), (3,3)],
        "resources": {"iron": 12, "minerals": 5},
        "battery_level": 70,
        "planet_time": 0,
        "color": "darkgray",
        "terrain_difficulty": 1.3
    }
}

class Spacecraft():
    
    def __init__(self, name, position = (0,0), battery = 100): 
        #we give the spacecraft a default position of 0,0 and a default battery of 100
        self.name = name
        self.position = position
        self.battery = battery
        
    def moveRover(self, direction, planet):
        #we will use the battery to move the rover in the NSEW directions
        #we will consider 1 unit on this scale to be about 1 km
        
        x, y = self.position
        if (direction == "N"):
            y += 1
        elif (direction == "S"):
            y -= 1
        elif (direction == "W"):
            x -= 1
        elif (direction == "E"):
            x += 1
        else:
            pass #no movement case
            
        #checking planet gride size
        max_x, max_y = planet["grid_size"]
        if not (0 <= x < max_x and 0 <= y < max_y): #if the position is not within the grid, we print error
           print(f"{self.name} cannot move. Position out of bounds.")
           return False
       
        if ((x,y) in planet["obstacles"]):
            print(f"{self.name} blocked by obstacle at ({x,y}).")
            return False
        
        self.position = (x, y) #assigning the updated position to the rover
        self.battery -= 1 * planet["terrain_difficulty"] #consuming battery according to movement and terrain difficulty
        print(f"{self.name} moved {direction} to {self.position}. Battery left: {self.battery:.1f}.")
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