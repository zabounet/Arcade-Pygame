# This repository contains a collection of arcade games
My goal is definitely not to recreate the games in the best way possible. 
The point is to experiment with game making (code, pixel arts, music and level design majorly).

## The recreated games are:
- Snake
- Pong
- Tetris

## The games of my own are :
- Chase

I plan to add more games in the future, including more ambitious ones. 
For now, I project to add the following:
- Flappy Bird
- Asteroids
- Pacman
- Space Invaders
- Breakout

## How to run the games
To run the games, you need to have Python 3.x installed on your machine.
you can download Python from the [official Python website](https://www.python.org/downloads/).

You can clone the repository and navigate into the folder of the game you want to play.
```bash
git clone
cd Arcade-Pygame/<game_name>/src
```
Then, you can install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
Then, you can run the games using the following command:
```bash
python main.py
```

## How to make an executable

As of now, only Snake is possible to make into an .exe file. To do so, use pyinstaller:
```bash
cd Snake/src
pyinstaller --clean main.spec
```