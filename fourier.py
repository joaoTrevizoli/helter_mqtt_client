import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt
from statistics import mean
def split_time_temp(string):
    return string[0:-1].split(" ")

time_temporary = []
time = []
measure = []
milliseconds = 0
iterator_control = 0
iterator_seconds_to_ms = []
with open("testes_ovino/cabresto_temp_91.txt", 'r') as f:
# with open("teste_bizerro/cabresto_temp_30_s.txt", 'r') as f:
    initial_time = 0
    for i in f:
        measure_time, temperature = split_time_temp(i)
        if len(time_temporary) == 0:
            time_temporary.append(0.)
            initial_time = float(measure_time)
        else:
            time_temporary.append(float(measure_time) - initial_time)
        measure.append(float(temperature))

for i in time_temporary:
    iterator_control += 1
    splits = 0
    measure_time = i
    try:
        measure_time_1 = time_temporary[iterator_control]
        if measure_time == measure_time_1:
            iterator_seconds_to_ms.append(measure_time)
        else:
            iterator_seconds_to_ms.append(measure_time)
            if len(iterator_seconds_to_ms) > 0:
                n_of_splits = 1.0 / len(iterator_seconds_to_ms)
                for j in iterator_seconds_to_ms:
                    time.append(j + splits)
                    splits += n_of_splits
                iterator_seconds_to_ms = []

    except Exception as e:
        iterator_seconds_to_ms.append(measure_time)
        if len(iterator_seconds_to_ms) > 0:
            n_of_splits = 1.0 / len(iterator_seconds_to_ms)
            for j in iterator_seconds_to_ms:
                time.append(j + splits)
                splits += n_of_splits
            iterator_seconds_to_ms = []

time = time
m = measure.copy()
measure = [(i - min(m))/(max(m) - min(m)) for i in m]

print(measure)
fig, ax = plt.subplots()
ax.plot(time, measure)
ax.set_xlabel('Time')
ax.set_ylabel('Signal amplitude')
fig.show()

plt.scatter(time, measure)
plt.show()

print(measure)

X = fftpack.fft(measure)

X_psd = np.abs(X)**2

print(X_psd)

freqs = fftpack.fftfreq(len(X_psd), 1./960)
print(freqs)

fig_2, ax_2 = plt.subplots()
# ax_2.set_xticks(np.arange(min(freqs), max(freqs)+1, 1.0))
ax_2.stem(freqs, np.abs(X))


fig_2.show()

i = freqs > 0

fig_2, ax_2 = plt.subplots()
ax_2.stem(i, np.abs(i))
fig_2.show()

fig3, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.plot(freqs[i], 10 * np.log10(X_psd[i]))
ax.set_xlabel('Frequency (1/minute)')
ax.set_ylabel('PSD (dB)')

fig3.show()

temp_fft_bis = X.copy()
temp_fft_bis[np.abs(X) > 0.001041667] = 0

temp_slow = np.real(fftpack.ifft(temp_fft_bis))
fig, ax = plt.subplots(1, 1, figsize=(6, 3))
# measure.plot(ax=ax, lw=.5)
ax.plot(time, temp_slow, '-')
ax.set_xlabel('Seconds')
ax.set_ylabel('Mean temperature')
fig.show()