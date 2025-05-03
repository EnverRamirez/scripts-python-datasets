import pandas as pd
import matplotlib.pyplot as plt

# Dados de exemplo
precos = [105, 110, 115, 120, 125, 130, 135, 130, 125, 120]
dias = range(len(precos))

# Calcular médias móveis
sma_5 = pd.Series(precos).rolling(5).mean()
ema_5 = pd.Series(precos).ewm(span=5).mean()

# Plotar
plt.plot(dias, precos, label='Preço')
plt.plot(dias, sma_5, label='SMA 5 dias')
plt.plot(dias, ema_5, label='EMA 5 dias')
plt.legend()
plt.show()
