import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from scipy.signal import medfilt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import binascii
import os

window = tk.Tk()
window.title('Файл не выбран')
window.minsize(640,480)

#fill_size = [0,75,65,170,170,1000]
fill_size = [0,10,0,10,0,10]

def func(x, a, b, c, d):
	return a * np.exp(-b*x**3+c*x+d)

def update_threshold0(value):
	value_0_0.config(to=value)
	value_0_1.config(to=value)

def update_threshold1(value):
	value_1_0.config(to=value)
	value_1_1.config(to=value)

def update_threshold2(value):
	value_2_0.config(to=value)
	value_2_1.config(to=value)

def update_value0_0(value):
	value = int(value)
	if value > fill_size[1]:
		return
	fill_size[0] = value
	draw_plots()
	
def update_value0_1(value):
	value = int(value)
	if value - fill_size[0] < 10:
		return
	fill_size[1] = value
	draw_plots()

def update_value1_0(value):
	value = int(value)
	if value > fill_size[3]:
		return
	fill_size[2] = value
	draw_plots()
	
def update_value1_1(value):
	value = int(value)
	if value - fill_size[2] < 10:
		return
	fill_size[3] = value
	draw_plots()

def update_value2_0(value):
	value = int(value)
	if value > fill_size[5]:
		return
	fill_size[4] = value
	draw_plots()
	
def update_value2_1(value):
	value = int(value)
	if value - fill_size[4] < 10:
		return
	fill_size[5] = value
	draw_plots()

file_name = str()
array = np.arange(1000)
fit_graf = np.zeros(1000)

def save_values():
	global file_name
	threshold_list = [threshold_slider0.get()
			  , threshold_slider1.get()
			  , threshold_slider2.get()]
	file = open(file_name, 'wb')
	for _ in range(0, len(fill_size)):
		file.write(binascii.unhexlify(hex(fill_size[_])[2:].zfill(4)))
	for _ in range(0, 3):
		file.write(binascii.unhexlify(hex(threshold_list[_])[2:].zfill(4)))
	file.close()
	fig = go.Figure()
	kEv = np.arange(1000)
	fig.add_trace(go.Scatter(x=kEv, y=array, mode='lines', name='tl_2',line=dict(color='rgb(119,221,231)')))
	fig.add_trace(go.Scatter(x=kEv, y=fit_graf, mode='lines', name='tl-204_1',line=dict(color="rgb(0,0,255)")))
	fig.update_layout(title=file_name,xaxis_title='Канал',yaxis_title='Количество частиц')
	fig.write_html(file_name.split('.')[0]+'_fit.html')
	
def update_values(check_values):
	global fill_size
	file = open(check_values, 'rb')
	values = list()
	for _ in range(0, 9):
		values.append(int(binascii.hexlify(file.read(2)), 16))
	value_0_0.set(values[0])
	value_0_1.set(values[1])
	value_1_0.set(values[2])
	value_1_1.set(values[3])
	value_2_0.set(values[4])
	value_2_1.set(values[5])
	threshold_slider0.set(values[6])
	threshold_slider1.set(values[7])
	threshold_slider2.set(values[8])
	fill_size = values
	file.close()

def open_array():
	global array, file_name
	file_path = filedialog.askopenfilename(filetypes=[("NumPy Array", f"*.npy")])
	if len(file_path) == 0:
		return
	filename = file_path.split('/')[-1]
	check_values = filename.split('.')[0]+".sth" # sth - something
	file_name = check_values
	if os.path.exists(check_values):
		update_values(check_values)
	window.title("Данные из массива: {}".format(filename))
	array = medfilt(np.load(file_path),kernel_size=1)[:1000]
	max_y = max(array)
	line.set_ydata(array)
	ax.set_ylim(ax.get_ylim()[0], max_y)
	draw_plots()

def draw_plots():
	global fit_graf
	colors =['rgb(205,0,205)','rgb(0,0,255)','rgb(119,221,231)']
	line_size = [2,4,6]
	fil = 1
	start_tl = fill_size[0]
	stop_tl = fill_size[1]
	start_t2 = fill_size[2]
	stop_t2 = fill_size[3]
	start_t3 = fill_size[4]
	stop_t3 = fill_size[5]
	xdata = np.arange(start_tl,stop_tl)
	ydata = array[start_tl:stop_tl]
	xdata1 = np.arange(start_t2,stop_t2)
	ydata1 = array[start_t2:stop_t2]
	xdata2 = np.arange(start_t3,stop_t3)
	ydata2 = array[start_t3:stop_t3]
	popt, pcov = curve_fit(func, xdata, ydata, p0=(0,0,0,0))
	popt1, pcov1 = curve_fit(func, xdata1, ydata1, p0=(0,0,0,0))
	popt2, pcov2 = curve_fit(func, xdata2, ydata2, p0=(0,0,0,0))
	fit = func(xdata, *popt)
	fit1 = func(xdata1, *popt1)
	fit2 = func(xdata2, *popt2)
	fit_graf[start_tl:stop_tl] = fit
	fit_graf[start_t2:stop_t2] = fit1
	fit_graf[start_t3:stop_t3] = fit2
	line2.set_ydata(fit_graf)
	plt.legend()
	canvas.draw_idle()

frame_plot = tk.Frame(window)\
.pack()

x = np.arange(1000)
y = np.zeros(1000)

fig, ax = plt.subplots()
line, = ax.plot(x, y, label = "tl_240", color="#A0C0F0")
line2, = ax.plot(x, y, label = "fit_graph", color="green")

canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
frame_button_1 = tk.Frame(window)
frame_button_1.pack(anchor=tk.NW)

text1 = tk.Label(frame_button_1, text="Нижняя Граница")
text1.pack(padx=70, pady=10, side=tk.LEFT)
text2 = tk.Label(frame_button_1, text="Верхняя Граница")
text2.pack(padx=0, side=tk.LEFT)
text2 = tk.Label(frame_button_1, text="Порог")
text2.pack(padx=70, side=tk.LEFT)

frame_button_2 = tk.Frame(window)
frame_button_2.pack(anchor=tk.NW)

text3 = tk.Label(frame_button_2, text="Канал 1")\
.pack(padx=10, side=tk.LEFT)

threshold0 = 1000
value_0_0 = tk.Scale(frame_button_2
                  , from_=0, to=threshold0
                  , orient=tk.HORIZONTAL
	          , length=100
                  , command=update_value0_0)
value_0_0.pack(padx=0, pady=0, side=tk.LEFT)
value_0_1 = tk.Scale(frame_button_2
                  , from_=10, to=threshold0
                  , orient=tk.HORIZONTAL
		  , variable=fill_size[1]
		  , length=100
                  , command=update_value0_1)
value_0_1.pack(padx=65, pady=0, side=tk.LEFT)
threshold_slider0 = tk.Scale(frame_button_2
                  , from_=0, to=1000
                  , orient=tk.HORIZONTAL
		  , length=100
                  , command=update_threshold0)
threshold_slider0.pack(padx=0, pady=0, side=tk.LEFT)
threshold_slider0.set(1000)

frame_button_3 = tk.Frame(window)
frame_button_3.pack(anchor=tk.NW)

threshold1 = 1000
text3 = tk.Label(frame_button_3, text="Канал 2")\
.pack(padx=10, side=tk.LEFT)
value_1_0 = tk.Scale(frame_button_3
                  , from_=0, to=threshold1
	          , orient=tk.HORIZONTAL
	          , length=100
                  , command=update_value1_0)
value_1_0.pack(padx=0, pady=0, side=tk.LEFT)
value_1_1 = tk.Scale(frame_button_3
                  , from_=10, to=threshold1
                  , orient=tk.HORIZONTAL
		  , length=100
                  , command=update_value1_1)
value_1_1.pack(padx=65, pady=0, side=tk.LEFT)
threshold_slider1 = tk.Scale(frame_button_3
                  , from_=0, to=1000
                  , orient=tk.HORIZONTAL
		  , length=100
                  , command=update_threshold1)
threshold_slider1.pack(padx=0, pady=0, side=tk.LEFT)
threshold_slider1.set(1000)

frame_button_4 = tk.Frame(window)
frame_button_4.pack(anchor=tk.NW)

threshold2 = 1000
text3 = tk.Label(frame_button_4, text="Канал 3")\
.pack(padx=10, side=tk.LEFT)
value_2_0 = tk.Scale(frame_button_4
                  , from_=0, to=threshold2
                  , orient=tk.HORIZONTAL
	          , length=100
                  , command=update_value2_0)
value_2_0.pack(padx=0, pady=0, side=tk.LEFT)
value_2_1 = tk.Scale(frame_button_4
                  , from_=10, to=threshold2
                  , orient=tk.HORIZONTAL
		  , length=100
                  , command=update_value2_1)
value_2_1.pack(padx=65, pady=0, side=tk.LEFT)
threshold_slider2 = tk.Scale(frame_button_4
                  , from_=0, to=1000
                  , orient=tk.HORIZONTAL
		  , length=100
                  , command=update_threshold2)
threshold_slider2.pack(padx=0, pady=0, side=tk.LEFT)
threshold_slider2.set(1000)

frame_button_5 = tk.Frame(window)
frame_button_5.pack(anchor=tk.NW)

button_open = tk.Button(frame_button_5, text="Открыть массив", width=15, command=open_array)\
.pack(padx=60, pady=10, side=tk.LEFT)

button_open = tk.Button(frame_button_5, text="Сохранить значения", width=15, command=save_values)\
.pack(padx=0, pady=10, side=tk.LEFT)

tk.mainloop()
