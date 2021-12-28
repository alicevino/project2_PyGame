import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg

import yfinance as yf
import matplotlib.pyplot as plt

import pylab

import pygame
from pygame.locals import *


plt.rcParams.update({
    "lines.marker": "o",         # available ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
    "lines.linewidth": "1.8",
    "axes.prop_cycle": plt.cycler('color', ['white']),  # line color
    "text.color": "white",       # no text in this example
    "axes.facecolor": "black",   # background of the figure
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",  # no labels in this example
    "axes.grid": "True",
    "grid.linestyle": "--",      # {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black", # color surrounding the plot
    "figure.edgecolor": "black",
})

fig = pylab.figure(figsize=[6, 6], # Inches
                   dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
                   )
fig.patch.set_alpha(0.1)

#ax = fig.gca()
#ax.plot([1, 2, 4])


data = yf.download('MSFT', '2021-11-10', '2021-12-10')
data['Adj Close'][0:50].plot()

canvas = agg.FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
#raw_data = renderer.tostring_rgb()
raw_data = renderer.buffer_rgba ()

pygame.init()

window = pygame.display.set_mode((600, 600), DOUBLEBUF)
screen = pygame.display.get_surface()
screen.fill('black')

size = canvas.get_width_height()

#surf = pygame.image.fromstring(raw_data, size, "RGB")
surf = pygame.image.frombuffer(raw_data, size, "RGBA")
screen.fill('black')
screen.blit(surf, (0,0))
pygame.display.flip()

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

