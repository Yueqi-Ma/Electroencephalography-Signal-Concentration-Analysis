import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

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
    nrow = 4  # Number of rows for subplots
    ncol = 1  # Number of columns for subplots
    fig, axs = plt.subplots(nrow, ncol, figsize=(10, 8))

    for Ichan in range(data.shape[1]):
        # Time-domain plot
        axs[0].plot(t_sec, data[:, Ichan] * 1e6)
        axs[0].set_xlim(t_sec[0], t_sec[-1])
        axs[0].set_ylim(-200, 200)
        axs[0].set_title('Channel ' + str(Ichan + 1))
        axs[0].set_xlabel('Time (sec)')
        axs[0].set_ylabel('Signal (uV)')

        # Extract alpha, beta, and gamma wave components
        alpha_mask = np.logical_and(t_sec >= alpha_range[0], t_sec <= alpha_range[1])
        beta_mask = np.logical_and(t_sec >= beta_range[0], t_sec <= beta_range[1])
        gamma_mask = np.logical_and(t_sec >= gamma_range[0], t_sec <= gamma_range[1])

        alpha_waveform = data[alpha_mask, Ichan]
        beta_waveform = data[beta_mask, Ichan]
        gamma_waveform = data[gamma_mask, Ichan]

        # Plot alpha, beta, and gamma wave time-domain waveforms
        axs[1].plot(t_sec[alpha_mask], alpha_waveform * 1e6, label='Alpha')
        axs[1].set_xlabel('Time (sec)')
        axs[1].set_ylabel('Signal (uV)')
        axs[1].set_title('Alpha Wave')

        axs[2].plot(t_sec[beta_mask], beta_waveform * 1e6, label='Beta')
        axs[2].set_xlabel('Time (sec)')
        axs[2].set_ylabel('Signal (uV)')
        axs[2].set_title('Beta Wave')

        axs[3].plot(t_sec[gamma_mask], gamma_waveform * 1e6, label='Gamma')
        axs[3].set_xlabel('Time (sec)')
        axs[3].set_ylabel('Signal (uV)')
        axs[3].set_title('Gamma Wave')

    plt.tight_layout()
    plt.show()