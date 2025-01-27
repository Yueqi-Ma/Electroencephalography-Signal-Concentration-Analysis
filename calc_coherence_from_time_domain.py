import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, coherence

def calc_coherence_from_time_domain(t_sec, data_V, fs, N, overlap, nave, t_analyze_sec, plots):
    data_V = data_V[:, 0:2]  # only examine the first two channels

    coherence = []
    wT = []
    f = []
    mean_cohere = []

    Ichan1 = 1
    Ichan2 = 2

    # Compute spectra
    fftx, wT, f = spectrogram(data_V[:, Ichan1], fs, window='hann', nperseg=N, noverlap=int(N*overlap))
    wT = wT + (N/2) / fs
    inds = np.where(f <= fs/2)[0]

    foo = data_V[:, Ichan2]
    ffty, _, _ = spectrogram(foo, fs, window='hann', nperseg=N, noverlap=int(N*overlap))
    wT = wT + (N/2) / fs

    # Compute coherence
    coherence, _, _ = coherence(fftx, ffty, fs, window='hann', nperseg=N, noverlap=int(N*overlap), nfft=N)
    wT = wT - (0.75 * nave * (1 - overlap) * N) / fs

    if plots:
        plt.imshow(coherence[inds, :].T, aspect='auto', origin='lower', extent=[min(wT), max(wT), min(f[inds]), max(f[inds])])
        plt.xlabel('Time (sec)')
        plt.ylabel('Frequency (Hz)')
        plt.title('Coherence')
        plt.clim(0, 1)
        plt.colorbar()

        if t_analyze_sec:
            for t_start, t_end in t_analyze_sec:
                plt.axvline(t_start, color='k', linestyle='--', linewidth=2)
                plt.axvline(t_end, color='k', linestyle='--', linewidth=2)

        plt.show()

    # Summarize data
    for t_start, t_end in t_analyze_sec:
        K = np.where((wT >= t_start) & (wT <= t_end))[0]
        mean_cohere.append(np.nanmedian(coherence[:, K], axis=1))

    return coherence, wT, f, np.array(mean_cohere).T