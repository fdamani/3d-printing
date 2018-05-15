
# coding: utf-8

# In[1]:


import numpy as np

import sys
sys.path.insert(0, '../data_processing/')
import gcode_to_train as gtt

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


# In[2]:


filename = "../../data/gcode/hans_solo_blaster_fill_density_10.gcode"
f = open(filename)
x = f.readlines()


# In[3]:


start_ind = gtt.cut_header(x)
end_ind = gtt.cut_footer(x)
num_commands = end_ind - start_ind

training_data = np.zeros((num_commands, 6))
x_trimmed = x[start_ind: end_ind]

train_raw = gtt.gcode_to_training_data(x_trimmed, training_data)

coordinates = train_raw[:,1:4]


#%matplotlib inline
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(coordinates[2:,0], coordinates[2:,1], coordinates[2:,2], s=.1)
fig = plt.figure(figsize=(10,10))
plt.show()
