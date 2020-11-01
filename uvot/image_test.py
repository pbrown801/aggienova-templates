# https://stackoverflow.com/questions/17835302/how-to-update-matplotlibs-imshow-window-interactively

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import os
import time

files=os.listdir('animation_images')
files_png = [f for f in files if (f.endswith('.png') and f.startswith("SN2005cs"))]
print(files_png)

# fig, ax = plt.subplots()
# fig.set_tight_layout(True)
# # mpimg image
# ax.set_xticks([])
# ax.set_yticks([])
# ax.set_title("Image: "+str(files_png[0]))
# plot_img = mpimg.imread(os.path.join('animation_images', files_png[0])) 
# show_img=ax.imshow(plot_img)

# V2
gs = gridspec.GridSpec(2, 2)

fig = plt.figure()
fig.set_tight_layout(True)

ax1 = fig.add_subplot(gs[0, 0]) 
ax1.plot([0,1])

ax2 = fig.add_subplot(gs[0, 1]) 
ax2.plot([0,1])
# mpimg image
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_title("Image: "+str(files_png[0]))
plot_img = mpimg.imread(os.path.join('animation_images', files_png[0])) 
show_img=ax2.imshow(plot_img)

ax3 = fig.add_subplot(gs[1, :])
ax3.plot([0,1])


def update(i):
    ax2.set_title("Image: "+str(files_png[i]))
    plot_img = mpimg.imread(os.path.join('animation_images', files_png[i])) 
    show_img.set_data(plot_img)


anim = FuncAnimation(fig, update, frames=np.arange(0,9), interval=500, repeat=True)
plt.show()