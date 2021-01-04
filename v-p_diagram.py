import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

Pressure  = {}
PressureP = {}
v = np.linspace(1, 2.5, 100)
R = 287.04
T = [200, 300, 400]
theta = [200, 300, 400]
powered1 = 1000 ** 0.286
powered2 = 1 / (-0.286 +1)
 
for t in T:
	Pressure[str(t)] = R * t / (v * 100)
for theta in theta:
	PressureP[str(theta)] = ((R * theta) / (v * 100 * powered1 )) ** powered2

P = pd.DataFrame(Pressure)
PT = pd.DataFrame(PressureP)

fig = plt.figure(figsize = [10, 10])

plt.plot(v, P['200'], c = 'b', ls = '--', label = "temperature")
plt.plot(v, P['300'], c = 'g', ls = '--')
plt.plot(v, P['400'], c = 'r', ls = '--')

plt.plot(v, PT['200'], c = 'b', label = "potential temperature")
plt.plot(v, PT['300'], c = 'g')
plt.plot(v, PT['400'], c = 'r')

plt.ylim([1000, 200])
plt.grid(True)

plt.legend(loc = 'upper right')
plt.annotate('T = 200K', (1.6, 310), fontsize = 15)
plt.annotate('T = 300K', (1.7, 440), fontsize = 15)
plt.annotate('T = 400K', (1.75, 580), fontsize = 15)

plt.title('v -p diagram', fontsize = 20)
plt.xlabel(r'v ($m^{3}Kg^{-1}$)', fontsize = 15)
plt.ylabel(r'-p ($mb$)', fontsize = 15)

plt.xlim(1.0,)
plt.xticks(fontsize = '10')
plt.yticks(fontsize = '10')
plt.savefig("v-p_diagram.png", bbox_inches = 'tight')
plt.show()