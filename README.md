# Cloth Simulation with Pygame

## Introduction

This code provides a basic 2D cloth simulation using the Pygame library. It demonstrates the use of Verlet integration to simulate the motion of particles, which are connected by sticks to create the appearance of a piece of cloth.

## Requirements

- Python
- Pygame library: To install, run `pip install pygame`.

## Components

### Particle

Each `Particle` object represents a point in the cloth, defined by its `x` and `y` position and its mass. Particles can be pinned in place (e.g., to simulate a piece of cloth pinned at the top).

### Stick

Each `Stick` object connects two particles and maintains a specific distance between them.

### Cloth

The `Cloth` class sets up the particles and sticks, and handles the update and rendering processes. It includes parameters like gravity, drag, and elasticity.

## Features

1. **Verlet Integration**: Used to simulate the motion of each particle in the cloth.
2. **Interactivity**: The cloth can interact with the mouse, allowing users to "cut" the cloth by dragging the mouse across it.
3. **Display Information**: The frame rate (FPS) and mouse position are displayed on screen.
4. **Customizability**: Cloth size, spacing between particles, gravity, drag, and other parameters can be easily modified for different effects.

## How to Run

1. Make sure you have Python and Pygame installed.
2. Run the code. You'll see a simulated cloth displayed in the window.
3. Click and drag your mouse across the cloth to cut and interact with it.
4. To exit, close the window or press `Ctrl+C` if running from a command line.

## Known Limitations

- The cloth simulation is basic and does not account for many real-world effects (e.g., friction, wind).
- Performance might degrade if the cloth has many particles or if there are many interactions in a short period.

## Future Improvements

- Implementing collision detection between the cloth and other objects.
- Optimizing the code for better performance.
- Adding more realistic physics effects like wind or turbulence.
- Implementing a more sophisticated method for cloth tearing.

## Credits

This project is created using the Pygame library. The cloth simulation logic is based on the principles of Verlet integration and basic physics equations.
