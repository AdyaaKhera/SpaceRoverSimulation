# Space Rover Simulation

A Python-based simulation that models rover and drone exploration across multiple planets.  
This project visualizes real-time vehicle movement, obstacle generation, solar charging, and experiment execution on simulated planetary surfaces.

---

## Features

### **Planet Environments**
Each planet includes:
- Terrain type  
- Grid size  
- Known + random obstacles  
- Natural resources  
- Battery limits  
- Terrain difficulty (affects rover energy use)  
- Sunlight hours (solar charging window)  
- Planet time tracking  
- Unique map color for visualization  

### **Vehicle Types**

#### **Rover**
- Ground movement (N/S/E/W)
- Battery usage depends on terrain difficulty
- Supports scientific instruments  
- **ExperimentRover** can perform experiments with randomized readings

#### **Drone**
- Aerial movement across the grid
- Ignores terrain difficulty
- Altitude control with limits  
- Higher altitude changes require more battery  

### **Mission System**
- Adds and manages vehicles  
- Progresses planetary time  
- Triggers solar charging  
- Randomly spawns new obstacles  
- Outputs detailed status reports  
- Logs all events to `mission_log.txt`

### **Real-Time Visualization**
Using `matplotlib`, the simulation animates:
- Planet grid  
- Obstacles  
- Rover and drone positions  
- Time updates per frame  

---

## Example Simulation Flow

The default script:
1. Loads **Mars**  
2. Creates a mission  
3. Adds:
   - Rover: **Pathfinder** (with camera)
   - Drone: **SkyScout**
4. Runs a ~50-frame animated simulation  
5. Logs events and shows planet map updates  

---

## Future Enhancements
Potential add-ons:
- A* or Dijkstra pathfinding for smart navigation
- Terrain weather simulation
- Vehicle-to-vehicle communication
- Resource extraction and base building
- Web-based dashboard or 3D visualization

---

# Created as the final project for CS 177 Course at Purdue University
