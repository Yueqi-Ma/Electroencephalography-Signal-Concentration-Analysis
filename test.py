import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, coherence

def windowedFFTPlot_spectragram(data, fs, Nfft, f_lim):
    n_per_page = 4
    nrow = int(np.ceil(n_per_page / 2))
    ncol = 2
    count = 0

    t_sec = np.arange(data.shape[0]) / fs

    fig, axes = plt.subplots(nrow, ncol, figsize=(10, 12))
    fig.subplots_adjust(hspace=0.5)

    for i in range(data.shape[1]):
        if count == 0:
            ax = axes[0, 0]
        else:
            ax = axes[count // ncol, count % ncol]

        f, Pxx = signal.welch(data[:, i], fs=fs, nperseg=Nfft)
        f = f[:len(Pxx)]
        Pxx = Pxx[:len(f_lim)]

        ax.plot(f, Pxx)
        ax.set_xlim(f_lim)
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power Spectral Density')
        ax.set_title('Channel {}'.format(i + 1))

        count += 1

        if count >= n_per_page:
            break

    plt.show()

def calcCoherence_fromTimeDomain(data, fs, Nfft, f_lim, compare_chan):
    n_per_page = 4
    nrow = int(np.ceil(n_per_page / 2))
    ncol = 2
    count = 0

    t_sec = np.arange(data.shape[0]) / fs

    fig, axes = plt.subplots(nrow, ncol, figsize=(10, 12))
    fig.subplots_adjust(hspace=0.5)

    for i in range(data.shape[1]):
        if count == 0:
            ax = axes[0, 0]
        else:
            ax = axes[count // ncol, count % ncol]

        f, Cxy = coherence(data[:, compare_chan[i, 0]], data[:, compare_chan[i, 1]],
                                  fs=fs, nperseg=Nfft)
        f = f[:len(Cxy)]

        ax.plot(f, Cxy)
        ax.set_xlim(f_lim)
        ax.set_ylim([0, 1])
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Coherence')
        ax.set_title('Channels {} and {}'.format(compare_chan[i, 0] + 1, compare_chan[i, 1] + 1))

        count += 1

        if count >= n_per_page:
            break

    plt.show()

# Set parameters
Nfft = 256
f_lim = [0, 100]
pname = 'SavedData/'
t_mark_sec = []
mark_names = {}
t_plot_sec = []
chan_names = {}
switch_case = 20

# Case 20
if switch_case == 20:
    fname = 'openBCI_raw_2014-04-23_06-52-48_Breakfast_Birds_CountBack.mat'
    sname = '2014-04-23 Breakfast, Web, Birds, Concentration'
    chan_names = ['Left Forehead', 'Right Forehead']
    t_mark_sec = [17 * 60 + 43, 21 * 60 + 31, 26 * 60 + 41 - 5, 29 * 60 + 23, 31 * 60 + 2]
    t_mark_sec = np.array([t_mark_sec[:-1], t_mark_sec[1:]]).T
    mark_names = ['Gaze Outside', 'Internet', 'Eyes Closed', 'Count Back by 3']
    if 1:
        t_mark_sec = np.insert(t_mark_sec, 0, [719, 967], axis=0)
        mark_names.insert(0, 'Internet')
    t_plot_sec = [680, 1890]





##################3############ Load data  ###############################################3
data = sio.loadmat(pname + fname)['data_uV']
fs = 250
count = data[:, 0]
data_V = data[:, 1:] * 1e-6
data_V = data_V[:, :2]  # Keep only the first two channels




# Filter data
data_V = data_V - np.mean(data_V, axis=0)
b, a = butter(2, [1, 100], fs=fs, btype='band')
data_V = filtfilt(b, a, data_V, axis=0)

# Analyze data
mean_data_V = np.mean(data_V, axis=0)
median_data_V = np.median(data_V, axis=0)
std_data_V = np.std(data_V, axis=0)
spread_data_V = np.diff(np.percentile(data_V, [0.5 - (0.68 - 0.5) / 2, 0.5 + (0.68 - 0.5) / 2], axis=0)) / 2
spread_data_V = np.median(spread_data_V) * np.ones_like(spread_data_V)

# Print results
print("Mean Data V:", mean_data_V)
print("Median Data V:", median_data_V)
print("Std Data V:", std_data_V)
print("Spread Data V:", spread_data_V)

# Perform required analysis using the data
# ...


# Perform required analysis using the data
compare_chan = np.array([[0, 1]])  # Specify the channels to compare
calcCoherence_fromTimeDomain(data_V, fs, Nfft, f_lim, compare_chan)
