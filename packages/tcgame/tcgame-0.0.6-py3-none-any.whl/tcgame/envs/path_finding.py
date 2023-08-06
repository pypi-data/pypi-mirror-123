"""
Reinforcement learning play environment - PathFinding
"""

import numpy as np
import time
import sys
import tkinter as tk
from PIL import Image, ImageTk

from os import path


class PathFinding(): 
    def __init__(self):
        self.window = tk.Tk()
        self.width = 6
        self.unit = 200
        self.height = 1
        img_path = path.join(path.dirname(__file__), 'assets')
        self.playerImgPath = path.join(img_path, 'player.png')
        self.endImgPath = path.join(img_path, 'flag.png')
        self.actions = ['left', 'right']
        self.n_actions = len(self.actions)
        self._build_maze()

    def _build_maze(self):
        self.distance = self.unit / 2 - 5
        self.centerx = self.centery = self.unit / 2
        self.imagew = self.imageh = self.unit - 10        
        self.window.title('Path Finding')
        self.img_player = ImageTk.PhotoImage(Image.open(self.playerImgPath).resize((self.imagew, self.imageh)))
        self.img_end = ImageTk.PhotoImage(Image.open(self.endImgPath).resize((self.imagew, self.imageh)))
        self.window.geometry('{0}x{1}'.format(self.width * self.unit, self.height * self.unit))
        self.canvas = tk.Canvas(self.window, bg='white',
                           height=self.height * self.unit,
                           width=self.width * self.unit)
        for c in range(0, self.width * self.unit, self.unit): 
            x0, y0, x1, y1 = c, 0, c, self.height * self.unit
            self.canvas.create_line(x0, y0, x1, y1) 
        origin = np.array([self.centerx, self.centery])
        oval_center = origin + np.array([self.unit * (self.width - 1), 0])
        self.oval = self.canvas.create_image(
            oval_center[0], oval_center[1], 
            image = self.img_end
            )
        self.rect = self.canvas.create_image(
            origin[0], origin[1],
            image = self.img_player
            )
        self.canvas.pack()

    def setMapSize(self, length=6, side=200):
        self.window.destroy()
        self.window = tk.Tk()
        self.width = length
        self.unit = side
        self.height = 1
        self._build_maze()

    def setPlayerImage(self, imgPath):
        self.playerImgPath = imgPath
        origin = np.array([self.centerx, self.centery])
        self.img_player = ImageTk.PhotoImage(Image.open(imgPath).resize((self.imagew, self.imageh)))
        self.rect = self.canvas.create_image(
            origin[0], origin[1],
            image = self.img_player
            )

    def setEndImage(self, imgPath):
        self.endImgPath = imgPath
        origin = np.array([self.centerx, self.centery])
        oval_center = origin + np.array([self.unit * (self.width - 1), 0])
        self.img_end = ImageTk.PhotoImage(Image.open(imgPath).resize((self.imagew, self.imageh)))
        self.oval = self.canvas.create_image(
            oval_center[0], oval_center[1], 
            image = self.img_end
            )

    def reset(self):
        self.window.update()
        # time.sleep(0.1)
        self.canvas.delete(self.rect) 
        origin = np.array([self.centerx, self.centery])
        self.rect = self.canvas.create_image(
            origin[0], origin[1],
            image = self.img_player
            )
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 'left':   # left
            if s[0] > self.unit:
                base_action[0] -= self.unit            
        elif action == 'right':   # right
            if s[0] < (self.width - 1) * self.unit:
                base_action[0] += self.unit
        self.canvas.move(self.rect, base_action[0], base_action[1])
        s_ = self.canvas.coords(self.rect) 
        if s_ == self.canvas.coords(self.oval):
            s_ = 'terminal'
            reward = 1
            done = True
        else:
            reward = 0
            done = False
        return s_, reward, done

    def render(self):
        # time.sleep(0.1)
        self.window.update()
