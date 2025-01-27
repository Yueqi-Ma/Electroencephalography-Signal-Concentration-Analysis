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
    nrow = 3  # Number of rows for subplots
    ncol = 1  # Number of columns for subplots
    fig, axs = plt.subplots(nrow, ncol, figsize=(10, 8))

    for Ichan in range(data.shape[1]):
        # Spectrogram
        f, t, pD = spectrogram(data[:, Ichan], fs=sample_rate, nperseg=500, noverlap=484)
        pD = 10 * np.log10(pD + 1e-10)  # Add a small constant to avoid zero values

        # Extract alpha, beta, and gamma wave components
        alpha_mask = np.logical_and(f >= alpha_range[0], f <= alpha_range[1])
        beta_mask = np.logical_and(f >= beta_range[0], f <= beta_range[1])
        gamma_mask = np.logical_and(f >= gamma_range[0], f <= gamma_range[1])

        alpha_power = pD[alpha_mask, :]
        beta_power = pD[beta_mask, :]
        gamma_power = pD[gamma_mask, :]

        # Plot alpha, beta, and gamma wave spectrograms
        axs[0].imshow(alpha_power, aspect='auto', origin='lower', extent=[t_sec[0], t_sec[-1], alpha_range[0], alpha_range[1]])
        axs[0].set_ylabel('Frequency (Hz)')
        axs[0].set_title('Alpha Wave')
        axs[0].set_xlabel('Time (sec)')

        axs[1].imshow(beta_power, aspect='auto', origin='lower', extent=[t_sec[0], t_sec[-1], beta_range[0], beta_range[1]])
        axs[1].set_ylabel('Frequency (Hz)')
        axs[1].set_title('Beta Wave')
        axs[1].set_xlabel('Time (sec)')

        axs[2].imshow(gamma_power, aspect='auto', origin='lower', extent=[t_sec[0], t_sec[-1], gamma_range[0], gamma_range[1]])
        axs[2].set_ylabel('Frequency (Hz)')
        axs[2].set_title('Gamma Wave')
        axs[2].set_xlabel('Time (sec)')

    plt.tight_layout()
    plt.show()