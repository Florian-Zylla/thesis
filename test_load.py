import os
import numpy as np
import matplotlib.pyplot as plt
os.chdir('/home/flo/thesis/log_files')
a =np.load('18.12.2019-18:26:02@acceleration_speed.npy')
print(a.shape)
plt.figure(dpi=300)
a[0,:]  = a[1,:]

plt.plot(a[:,5],a[:,6],marker='+',linewidth=0.5)
plt.plot(a[:,7],a[:,8],marker = 'x',linewidth= 0.5)
plt.plot(a[a.shape[0]-1,6],a[a.shape[0]-1,7], marker = 'o', ms=5)
plt.axis('equal')
plt.show()