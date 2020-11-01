# https://stackoverflow.com/questions/17835302/how-to-update-matplotlibs-imshow-window-interactively

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation
import os
import time

files=os.listdir('animation_images')
files_png = [f for f in files if (f.endswith('.png') and f.startswith("SN2005cs"))]
print(files_png)
fig, ax = plt.subplots()
fig.set_tight_layout(True)
# mpimg image
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Image: "+str(files_png[0]))
plot_img = mpimg.imread(os.path.join('animation_images', files_png[0])) 
show_img=ax.imshow(plot_img)


def update(i):
    ax.set_title("Image: "+str(files_png[i]))
    plot_img = mpimg.imread(os.path.join('animation_images', files_png[i])) 
    show_img.set_data(plot_img)


anim = FuncAnimation(fig, update, frames=np.arange(0,9), interval=500, repeat=True)
plt.show()