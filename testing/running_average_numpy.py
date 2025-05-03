import numpy as np
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

# Dados de exemplo (preços de ações)
precos = np.array([105.2, 106.5, 107.8, 108.3, 109.1, 
                   110.4, 109.7, 108.9, 108.5, 109.8])

# Calculando médias móveis
sma_3 = simple_moving_average(precos, 3)
wma_3 = weighted_moving_average(precos, 3)
ema = exponential_moving_average(precos, 0.2)

print("SMA(3):", sma_3)
print("WMA(3):", wma_3)
print("EMA:", ema)

plt.figure(figsize=(10, 5))
plt.plot(precos, 'o-', label='Preços Originais')
plt.plot(np.arange(2, len(precos)), sma_3, 's-', label='SMA(3)')
plt.plot(np.arange(2, len(precos)), wma_3, 'd-', label='WMA(3)')
plt.plot(ema, '^-', label='EMA (α=0.2)')
plt.legend()
plt.title('Comparação de Médias Móveis')
plt.xlabel('Dias')
plt.ylabel('Preço')
plt.grid(True)
plt.show()
