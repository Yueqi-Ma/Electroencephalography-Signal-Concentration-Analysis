import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

folder_path = r'D:/OneDrive - Macau University of Science and Technology/Desktop/MUST_year4A/FYP/concentration/WAVs'

# Get all WAV files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# Process each WAV file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    sample_rate, data = wavfile.read(file_path)

    # Ensure data is 2D array
    if data.ndim == 1:
        data = np.expand_dims(data, axis=1)

    # Analyze data
    mean_data_V = np.mean(data, axis=0)
    median_data_V = np.median(data, axis=0)
    std_data_V = np.std(data, axis=0)
    spread_data_V = np.diff(np.percentile(data, [0.5 + (0.68 - 0.5) * np.array([-1, 1])])) / 2

    # Plot data
    t_sec = np.arange(1, data.shape[0] + 1) / sample_rate
    nrow = max([2, data.shape[1]])
    ncol = 2
    ax = []
    fig = plt.figure()
    fig.set_size_inches(10, 8)

    for Ichan in range(data.shape[1]):
        # Time-domain plot
        ax1 = fig.add_subplot(nrow, ncol, (Ichan * 2) + 1)
        ax1.plot(t_sec, data[:, Ichan] * 1e6)
        ax1.set_xlim(t_sec[0], t_sec[-1])
        ax1.set_ylim(-200, 200)
        ax1.set_title('Channel ' + str(Ichan + 1))
        ax1.set_xlabel('Time (sec)')
        ax1.set_ylabel('Signal (uV)')
        ax.append(ax1)

        # Spectrogram
        ax2 = fig.add_subplot(nrow, ncol, (Ichan * 2) + 2)
        f, t, pD = spectrogram(data[:, Ichan], fs=sample_rate, nperseg=500, noverlap=484)
        pD = 10 * np.log10(pD + 1e-10)  # Add a small constant to avoid zero values
        im = ax2.imshow(pD, aspect='auto', origin='lower', extent=[t_sec[0], t_sec[-1], f[0], f[-1]])
        ax2.set_ylabel('Frequency (Hz)')
        ax2.set_title(file_name + ', Channel ' + str(Ichan + 1))
        ax2.set_xlabel('Time (sec)')
        ax.append(ax2)

    # Adjust subplot spacing and visibility
    plt.tight_layout(pad=1.0, h_pad=1.0)
    plt.subplots_adjust(hspace=0.5)
    plt.show()


