import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

folder_path = r'D:/OneDrive - Macau University of Science and Technology/Desktop/MUST_year4A/FYP/concentration/WAVs'

# Get all WAV files in the folder
file_list = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# Define frequency ranges for alpha, beta, and gamma waves
alpha_range = (8, 13)  # Alpha wave range (in Hz)
beta_range = (13, 30)  # Beta wave range (in Hz)
gamma_range = (30, 100)  # Gamma wave range (in Hz)

# Process each WAV file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    sample_rate, data = wavfile.read(file_path)

    # Ensure data is 2D array
    if data.ndim == 1:
        data = np.expand_dims(data, axis=1)

    # Analyze data
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

        # Extract alpha, beta, and gamma wave components
        alpha_mask = np.logical_and(f >= alpha_range[0], f <= alpha_range[1])
        beta_mask = np.logical_and(f >= beta_range[0], f <= beta_range[1])
        gamma_mask = np.logical_and(f >= gamma_range[0], f <= gamma_range[1])

        alpha_power = np.mean(pD[alpha_mask, :], axis=0)
        beta_power = np.mean(pD[beta_mask, :], axis=0)
        gamma_power = np.mean(pD[gamma_mask, :], axis=0)

        # Plot alpha, beta, and gamma waves
        fig2, ax3 = plt.subplots()
        ax3.plot(t, alpha_power, label='Alpha')
        ax3.plot(t, beta_power, label='Beta')
        ax3.plot(t, gamma_power, label='Gamma')
        ax3.set_xlabel('Time (sec)')
        ax3.set_ylabel('Power Spectral Density (dB/Hz)')
        ax3.set_title(file_name + ', Channel ' + str(Ichan + 1))
        ax3.legend()

    # Adjust subplot spacing and visibility
    plt.tight_layout(pad=1.0, h_pad=1.0)
    plt.show()