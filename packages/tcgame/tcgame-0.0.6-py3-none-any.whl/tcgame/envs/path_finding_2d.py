"""
Reinforcement learning play environment - Maze
"""

import numpy as np
import time
import sys
import tkinter as tk


UNIT = 150
MAZE_H = 4
MAZE_W = 4
DISTANCE = UNIT / 2 - 5


class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.actions = ['up', 'down', 'left', 'right']
        self.n_actions = len(self.actions)
        self.title('Maze')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)
        for c in range(0, MAZE_W * UNIT, UNIT): 
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
        origin = np.array([UNIT / 2, UNIT / 2])
        hell1_center = origin + np.array([UNIT * 2, UNIT])
        self.hell1 = self.canvas.create_rectangle(
            hell1_center[0] - DISTANCE, hell1_center[1] - DISTANCE,
            hell1_center[0] + DISTANCE, hell1_center[1] + DISTANCE,
            fill='black')
        hell2_center = origin + np.array([UNIT, UNIT * 2])
        self.hell2 = self.canvas.create_rectangle(
            hell2_center[0] - DISTANCE, hell2_center[1] - DISTANCE,
            hell2_center[0] + DISTANCE, hell2_center[1] + DISTANCE,
            fill='black')
        oval_center = origin + UNIT * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - DISTANCE, oval_center[1] - DISTANCE,
            oval_center[0] + DISTANCE, oval_center[1] + DISTANCE,
            fill='yellow')
        self.rect = self.canvas.create_rectangle(
            origin[0] - DISTANCE, origin[1] - DISTANCE,
            origin[0] + DISTANCE, origin[1] + DISTANCE,
            fill='red')
        self.canvas.pack()

    def reset(self):
        self.update()
        # time.sleep(0.1)
        self.canvas.delete(self.rect)
        origin = np.array([UNIT / 2, UNIT / 2])
        self.rect = self.canvas.create_rectangle(
            origin[0] - DISTANCE, origin[1] - DISTANCE,
            origin[0] + DISTANCE, origin[1] + DISTANCE,
            fill='red')
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 'up':
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 'down':
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        elif action == 'right':
            if s[0] < (MAZE_W - 1) * UNIT:
                base_action[0] += UNIT
        elif action == 'left':
            if s[0] > UNIT:
                base_action[0] -= UNIT
        self.canvas.move(self.rect, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.rect)
        if s_ == self.canvas.coords(self.oval):
            reward = 1
            done = True
            s_ = 'terminal'
        elif s_ in [self.canvas.coords(self.hell1), self.canvas.coords(self.hell2)]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        return s_, reward, done

    def render(self):
        # time.sleep(0.1)
        self.update()