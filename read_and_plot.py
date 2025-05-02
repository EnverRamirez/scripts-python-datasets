import numpy as np
import numpy.ma as ma
from datetime import datetime
import matplotlib.pyplot as plt

def simple_moving_average(data, window_size):
    """Calcula média móvel simples usando NumPy"""
    weights = np.ones(window_size) / window_size
    return np.convolve(data, weights, mode='valid')

def weighted_moving_average(data, window_size):
    """Calcula média móvel ponderada"""
    weights = np.arange(1, window_size + 1)
    return np.convolve(data, weights/weights.sum(), mode='valid')

def exponential_moving_average(data, alpha=0.3):
    """Calcula média móvel exponencial"""
    ema = np.zeros_like(data)
    ema[0] = data[0]
    for i in range(1, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i-1]
    return ema

#open data file
fname='SBBU.txt'

#read information of the data file
line_count = 0
with open(fname,'r') as file:
    for line in file:
        line_count += 1

#define precipitation, relative humidity and time
prec = np.empty([line_count], dtype = float)
ur = np.empty([line_count], dtype = float)
timestamp = np.empty([line_count], dtype = float)


#open data file to ingest information
f=open(fname, 'r')

#ingest info
idx=0
for line in f:
     line = line.strip()
     cols = line.split(';')
     prec[idx]=float(cols[6])
     ur[idx]=float(cols[5])
     date_str=str(cols[4].strip())
     dt=datetime.strptime(date_str, "%Y-%m-%d")
     year = dt.year
     day_of_year = dt.timetuple().tm_yday  # Day of year (1-366)
     frac_of_year = day_of_year / (366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365)
     timestamp[idx] = year + frac_of_year
     idx += 1

#indicate NaNs
prec[prec == -9999.0] = np.nan
ur[ur == -9999.0] = np.nan

#Compute running average
# Calculando médias móveis com diferentes janelas
wl3=3
wl7=7
wl10=10
wl30=30
sma_3 = simple_moving_average(ur, wl3)
sma_7 = simple_moving_average(ur, wl7)
sma_10 = simple_moving_average(ur, wl10)
sma_30 = simple_moving_average(ur, wl30)

#compute a polynomial fit
msked_y = ma.masked_invalid(ur)
msked_x = ma.masked_where(ma.getmask(msked_y), timestamp)
slope, intercept = ma.polyfit(msked_x, msked_y, 1)

trend_30 = slope * timestamp + intercept

plt.figure(figsize=(10, 5))
plt.plot(ur, 'o-', label='Umidade Relativa')
#plt.plot(np.arange(wl3-1, len(ur)), sma_3, '-', label='SMA(3)')
plt.plot(np.arange(wl7-1, len(ur)), sma_7, 's-', label='SMA(7)')
#plt.plot(np.arange(wl10-1, len(ur)), sma_10, '-', label='SMA(10)')
plt.plot(np.arange(wl30-1, len(ur)), sma_30, 's-', label='SMA(30)')

#plt.plot(np.arange(2, len(precos)), sma_30, 's-', label='SMA(30)')
#plt.plot(np.arange(2, len(precos)), wma_3, 'd-', label='WMA(3)')
#plt.plot(ema, '^-', label='EMA (α=0.2)')

plt.plot(timestamp, trend_30, 's-', label='trend(30)')

plt.legend()
plt.title('Comparação de Médias Móveis')
plt.xlabel('Dias')
plt.ylabel('Umidade Relativa')
plt.grid(True)
plt.show()

##plot the data (use EC_indexes scripts as references)
#fig,(ax,ax2)=plt.subplots(2)
#
#ax.plot(timestamp, ur, color="black")
#ax.set_title('Umidade Relativa (%)')
#ax.spines['bottom'].set_visible(True)
#
#ax2.plot(timestamp, prec, color="blue")
#ax2.set_title('Precipitação (mm/day)')
#ax.label_outer()
#
##plt.plot(timestamp, ur)
#station=cols[0].strip()+" ("+cols[1].strip()+" Lat: "+cols[2].strip()+" Lon: "+cols[3].strip()+")"
#fig.suptitle(station,fontsize=13)
##plt.tight_layout()
#plt.show()
