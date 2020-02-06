# NEAT Asteroids
## Overview
This project involves implementing the NEAT algorithm to play the Asteroids arcade game. The aim of this project was to use the NEAT algorithm to train a neural network to beat a high score of 250 asteroids destroyed without colliding with an asteroid. The code for this project allows you to see different species in each generation and examine the different techniques used by each until they collide with an asteroid. I have also included a complete Asteroids game for you to try and beat the AI with, to make this challenge easier you have 3 lives while the AI only has one life. Examples of different species that are possible to be produced are given below. This species uses the thruster and spins as it moves.

![alt-text](https://github.com/invicta117/asteroid-potato/blob/master/loopy_ship.gif)

This species is a lot more directional in it's movements

![alt-text](https://github.com/invicta117/asteroid-potato/blob/master/directional_ship.gif)

Finally the predominant species does not move and instead has a lot more precise. This species with some training can reach the 250 asteroids destroyed in one game.

![alt-text](https://github.com/invicta117/asteroid-potato/blob/master/stationary_ship.gif)

Inputs to the network include distance to the 5 closest asteroids, angle between the ship and asteroid as well as the asteroids velocity.

## How to Implement

This project was built using Python 3.6 and uses the following

Neat:	0.92

Numpy:	1.18.0

Pygame:	1.9.6

Matplotlib:     3.1.2
