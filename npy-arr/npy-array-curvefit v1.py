import time
import numpy as np
import matplotlib.pyplot as plt
#import plotly.express as px
import plotly.graph_objects as go
from scipy.signal import medfilt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit

def func(x, a, b, c, d):
	return a * np.exp(-b*x**3+c*x+d)

colors =['rgb(205,0,205)','rgb(0,0,255)','rgb(119,221,231)'] #цвет линии b g r 
line_size = [2,4,6] # ширина линии графика
kEv = np.arange(1000)
fit_graf = np.zeros(1000)
tl_240 = np.load('eu_1.npy')[:1000]
tl_max = medfilt(tl_240,kernel_size=1)[:1000]
tl_max_1, tl_max_2 = max(tl_max[:100]), max(tl_max[100:])
print(tl_max_1, tl_max_2)
where_1 = np.where(tl_max==tl_max_1)[0]
where_2 = np.where(tl_max==tl_max_2)[0]
index_1 = where_1[len(where_1)//2]
index_2 = where_2[len(where_2)//2]
low_index = (np.where(tl_max==min(tl_max[index_1:index_2]))[0][0]-index_1)//2
print(low_index)
print(where_1[len(where_1)//2], where_2[len(where_2)//2])
print(index_1+low_index, index_1-low_index)
start_tl = 0
stop_tl = index_1+low_index
start_t2 = index_1+low_index-6
stop_t2 = index_2-35
start_t3 = index_2-37
stop_t3 = 1000
xdata = np.arange(start_tl,stop_tl)
ydata = tl_240[start_tl:stop_tl]
xdata1 = np.arange(start_t2,stop_t2)
ydata1 = tl_240[start_t2:stop_t2]
xdata2 = np.arange(start_t3,stop_t3)
ydata2 = tl_240[start_t3:stop_t3]
popt, pcov = curve_fit(func, xdata, ydata, p0=(0,0,0,0))
popt1, pcov1 = curve_fit(func, xdata1, ydata1, p0=(0,0,0,0))
popt2, pcov2 = curve_fit(func, xdata2, ydata2, p0=(0,0,0,0))
fit = func(xdata, *popt)
fit1 = func(xdata1, *popt1)
fit2 = func(xdata2, *popt2)
fit_graf[start_tl:stop_tl] = fit
fit_graf[start_t2:stop_t2] = fit1
fit_graf[start_t3:stop_t3] = fit2
#print(func(xdata, *popt))
str_ = 'Tl-204 756 kev   ' +'a='+str(popt[0])+' b='+str(popt[1])+' c='+str(popt[2])+' d='+str(popt[3])
fig = go.Figure()
fig.add_trace(go.Scatter(x=kEv, y=tl_240, mode='lines', name='tl_2',line=dict (color=colors[1])))
fig.add_trace(go.Scatter(x=kEv, y=fit_graf, mode='lines', name='tl-204_1',line=dict (color=colors[2])))
plt.plot(kEv, tl_240, label = "raw", color="red")
plt.plot(kEv, fit_graf, label = "fit_graph", color="green")
plt.legend()
plt.show()#отображаем, x=kEv, а y=данные из fit_graf
fig.update_layout(title=str_,xaxis_title='kанал',yaxis_title='количество частиц')
fig.write_html('fit.html')
