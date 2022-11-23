import matplotlib
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

columns = ['data', 'moeda_1', 'moeda_2', 'moeda_3', 'moeda_4', 'moeda_5', 'moeda_6']
forex = pd.read_table('forex.txt', delim_whitespace=True, names=columns)
forex = forex.drop('data', axis=1)

# Variations in fores
d_forex = pd.DataFrame(columns=columns[1:])
for current, next in zip(forex[:-1].items(), forex[1:].items()):
    coil_name = current[0]
    d_forex[coil_name] = np.array(next[1]) - np.array(current[1])

# X Correlation calculation
x_correlation_data = {}
for i, coil in enumerate(columns):
    if coil not in ['data', 'moeda_1'] and i < len(columns):
        fig = plt.figure()
        plt.title(coil)
        ax1 = fig.add_subplot(211)
        ax1.xcorr(d_forex['moeda_1'], d_forex[coil], usevlines=True, maxlags=5, normed=True, lw=2)
        ax1.grid(True)
        ax1.axhline(0, color='blue', lw=2)
        y_max = ax1.dataLim.ymax
        y_min = ax1.dataLim.ymin
        plt.show()


# Apply lag method
def apply_lag(vec, lag):
    vec = list(vec)
    if lag > 0:
        for _ in range(lag):
            vec.insert(0, 0)
            vec.pop()
    else:
        vec = vec[abs(lag):]
        for _ in range(abs(lag)):
            vec.append(0)
    return np.array(vec)


# Visual analysis for x correlation plots
lags = {
    'moeda_2': 0,
    'moeda_3': 10,
    'moeda_4': -5,
    'moeda_5': 0
}

# Apply lag to original forex data
for moeda in lags:
    forex[moeda] = apply_lag(forex[moeda], lags[moeda])
