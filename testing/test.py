import numpy as np
import numpy.ma as ma
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

#filt_length=7
#filt_data = simple_moving_average(precos, filt_length)
#msked_y = ma.masked_invalid(filt_data)
#msked_x = ma.masked_where(ma.getmask(msked_y), timestamp[filt_length-1:])
#slope_filt, intercept_filt = ma.polyfit(msked_x, msked_y, 1)

# Dados de exemplo (preços de ações)
precos = np.array([152, 153, 155, 154, 156, 158, 159, 157, 155, 153, 
                   154, 156, 158, 160, 162, 161, 163, 165, 164, 166,
                   165, 160, 155, 157, 157, 153, 155, 158, 159, 160,
                   157, 158, 159, 160, 163, 158, 154, 160, 163, 161])

timestamp=np.zeros_like(precos)
for i in range(1, len(precos)):
   timestamp[i] = i

#timestamp=np.arange(len(precos))

# Calculando médias móveis com diferentes janelas
wl3=3
wl7=7
wl10=10
wl30=30
sma_3 = simple_moving_average(precos, wl3)
sma_7 = simple_moving_average(precos, wl7)
sma_10 = simple_moving_average(precos, wl10)
sma_30 = simple_moving_average(precos, wl30)
#wma_3 = weighted_moving_average(precos, 3)
#ema = exponential_moving_average(precos, 0.2)

#compute a polynomial fit of full data
msked_y = ma.masked_invalid(precos)
msked_x = ma.masked_where(ma.getmask(msked_y), timestamp)
slope, intercept = ma.polyfit(msked_x, msked_y, 1)

trend = slope * timestamp + intercept

#compute a polynomial fit of fluctuations filtered data
#  It was tested to eventually becomes a python object (function)
#    - with filt_length it was removed data as a result of running mean procedure
#    - running mean filters fluctuations
#    - although the trend is able to include data from the begining, with "[filt_length-1:]" was removed from plot for clarity
filt_length=7
filt_data = simple_moving_average(precos, filt_length)
msked_y = ma.masked_invalid(filt_data)
msked_x = ma.masked_where(ma.getmask(msked_y), timestamp[filt_length-1:])
slope_filt, intercept_filt = ma.polyfit(msked_x, msked_y, 1)

trend_30 = slope_filt * timestamp + intercept_filt

#implemented a function to compute linear trend for fluctuations filtered data
window=3
ftrend=linear_trend_of_moving_averaged_data(timestamp, precos, window)

#plt.figure(figsize=(10, 5))
#plt.plot(precos, 'o-', label='Umidade Relativa')
##plt.plot(np.arange(wl3-1, len(ur)), sma_3, '-', label='SMA(3)')
#plt.plot(np.arange(wl7-1, len(precos)), sma_7, 's-', label='SMA(7)')
##plt.plot(np.arange(wl10-1, len(ur)), sma_10, '-', label='SMA(10)')
#plt.plot(np.arange(wl30-1, len(precos)), sma_30, 's-', label='SMA(30)')
#
##plt.plot(np.arange(2, len(precos)), sma_30, 's-', label='SMA(30)')
##plt.plot(np.arange(2, len(precos)), wma_3, 'd-', label='WMA(3)')
##plt.plot(ema, '^-', label='EMA (α=0.2)')
#
#plt.plot(timestamp, trend_30, 's-', label='trend(30)')

print("SMA(3):", sma_3)
print("SMA(7):", sma_7)
print("SMA(10):", sma_10)
print("SMA(30):", sma_30)
#print("WMA(3):", wma_3)
#print("EMA:", ema)

plt.figure(figsize=(10, 5))
plt.plot(precos, 'o-', label='Preços Originais')
plt.plot(np.arange(wl3-1, len(precos)), sma_3, 's-', label='SMA(3)')
plt.plot(np.arange(wl7-1, len(precos)), sma_7, 's-', label='SMA(7)')
plt.plot(np.arange(wl10-1, len(precos)), sma_10, 's-', label='SMA(10)')
plt.plot(np.arange(wl30-1, len(precos)), sma_30, 's-', label='SMA(30)')
plt.plot(trend, 's-', label='LREG(0)')

# Plot the trend 
#    - with filt_length it was removed data as a result of running mean procedure
#    - running mean filters fluctuations
#    - although the trend is able to include data from the begining, with "[filt_length-1:]" was removed from plot for clarity
plt.plot(timestamp[filt_length-1:], trend_30[filt_length-1:], 's-', label='LREG('+str(filt_length)+')')

plt.plot(timestamp[window-1:], ftrend[window-1:], 's-', label='LREG('+str(window)+')')


plt.legend()
plt.title('Comparação de Médias Móveis')
plt.xlabel('Dias')
plt.ylabel('Preço')
plt.grid(True)
plt.show()
