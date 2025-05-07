for x in $(ls ../merge_e_samet/*CSV)
do
  ls $x

  cat >  read_and_plot_merge_e_samet.py <<EOF
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

def linear_trend_of_moving_averaged_data(xdata,ydata, window):
    """ Calcula a tendência lineal de dados filtrados com running average """
    if window >= 1:
       print()
       #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window-1:])
       #local_window=window-1
    #elif window == 0:
       #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window:])
    #   local_window=0
    elif window <= 0:
       print('Error: window for average must be at least one')
       return

    filt_data = simple_moving_average(ydata, window)
    msked_y = ma.masked_invalid(filt_data)
    msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window-1:])
    #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[local_window:])
    slope, intercept = ma.polyfit(msked_x, msked_y, 1)
    ltrend = slope * xdata + intercept
    return ltrend

def slope_of_linear_trended_moving_averaged_data(xdata,ydata, window):
    """ Calcula o slope da tendência lineal de dados filtrados com running average """
    if window >= 1:
       print()
       #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window-1:])
       #local_window=window-1
    #elif window == 0:
       #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window:])
    #   local_window=0
    elif window <= 0:
       print('Error: window for average must be at least one')
       return

    filt_data = simple_moving_average(ydata, window)
    msked_y = ma.masked_invalid(filt_data)
    msked_x = ma.masked_where(ma.getmask(msked_y), xdata[window-1:])
    #msked_x = ma.masked_where(ma.getmask(msked_y), xdata[local_window:])
    slope, intercept = ma.polyfit(msked_x, msked_y, 1)
    return slope

#open data file
fname='../merge_e_samet/Bauru.CSV'
fname='$x'

#read information of the data file
line_count = 0
with open(fname,'r') as file:
    next(file)   #skip the header line
    for line in file:
        line_count += 1

#define precipitation, relative humidity and time
prec = np.empty([line_count], dtype = float)
tmax = np.empty([line_count], dtype = float)
timestamp = np.empty([line_count], dtype = float)


#open data file to ingest information
with open(fname, 'r') as f:
  next(f)
  #f=open(fname, 'r')
  #ingest info
  idx=0
  for line in f:
        line = line.strip()
        cols = line.split(',')
        prec[idx]=float(cols[1])
        tmax[idx]=float(cols[2])
        date_str=str(cols[0].strip())
        dt=datetime.strptime(date_str, "%b%Y")
        #year = dt.year 
        #day_of_year = dt.timetuple().tm_yday  # Day of year (1-366)
        #frac_of_year = day_of_year / (366 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 365)
        #timestamp[idx] = year + frac_of_year
        timestamp[idx] = dt.year + dt.month / 12.
        idx += 1

#indicate NaNs
prec[prec == -9999.0] = np.nan
tmax[tmax == -9999.0] = np.nan

#Compute running average
# Calculando médias móveis com diferentes janelas
wl3=3
wl7=7
wl10=10
wl30=30
sma_3 = simple_moving_average(tmax, wl3)
sma_7 = simple_moving_average(tmax, wl7)
sma_10 = simple_moving_average(tmax, wl10)
sma_30 = simple_moving_average(tmax, wl30)

#compute a linear trend for the full data
msked_y = ma.masked_invalid(tmax)
msked_x = ma.masked_where(ma.getmask(msked_y), timestamp)
slope, intercept = ma.polyfit(msked_x, msked_y, 1)

trend = slope * timestamp + intercept

#window is related to the data frequency, is the data is monthly then window=3 means filter below 3 month fluctuations
window=3 #180
ftrendPrec=linear_trend_of_moving_averaged_data(timestamp, prec, window)
slopePrec=slope_of_linear_trended_moving_averaged_data(timestamp, prec, window)

ftrendTmax=linear_trend_of_moving_averaged_data(timestamp, tmax, window)
slopeTmax=slope_of_linear_trended_moving_averaged_data(timestamp, tmax, window)

#plt.figure(figsize=(10, 5))
#plt.plot(timestamp, tmax, 'o-', label='Umidade Relativa')
#plt.plot(timestamp, trend, 's-', label='trend(30)')
#plt.plot(timestamp[window-1:], ftrend[window-1:], 's-', label='LREG('+str(window)+')')
#
#plt.legend()
#plt.title('Comparação de Médias Móveis')
#plt.xlabel('Month') #('Dias')
#plt.ylabel('Umidade Relativa')
#plt.grid(True)
#plt.show()

#plot the data (use EC_indexes scripts as references)
fig,(ax,ax2)=plt.subplots(2)

ax.plot(timestamp, tmax, color="black")
ax.plot(timestamp, ftrendTmax, 's-', label='trend('+str(window)+')', color="red")
ax.set_title('Temperatura maxima (C) '+'trend: '+str(round(slopeTmax,3)))
ax.spines['bottom'].set_visible(True)

ax2.plot(timestamp, prec, color="blue")
ax2.plot(timestamp, ftrendPrec, 's-', label='trend('+str(window)+')', color="red")
ax2.set_title('Precipitação (mm/day) '+'trend: '+str(round(slopePrec,3)))
ax.label_outer()

#plt.plot(timestamp, tmax)
#station=fname.strip #cols[0].strip()+" ("+cols[1].strip()+" Lat: "+cols[2].strip()+" Lon: "+cols[3].strip()+")"
#station=fname.split('/')[-1:]
station=''.join(''.join(fname.split('/')[-1:]).split('.CSV')[0])
fig.suptitle(station,fontsize=13)
#plt.tight_layout()
#plt.show()
print("../plot_merge_e_samet/"+station+".png")
plt.savefig("../plot_merge_e_samet/"+station+".png")
plt.close()
EOF

python3 read_and_plot_merge_e_samet.py
#Removing indent
#awk '{sub(/^[ \t]+/, ""); print}' temp.py > read_and_plot_merge_e_samet.py

done
