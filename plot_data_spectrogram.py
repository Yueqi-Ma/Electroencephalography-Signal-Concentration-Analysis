import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram, coherence


def plot_data_spectrogram(data_V, fs, t_plot_sec=None, n_per_page=8, nrow=3, ncol=1, chan_names=None,
                          t_mark_sec=None, t_analyze_sec=None, f_lim=None):
    t_sec = np.arange(len(data_V)) / fs
    #t = np.arange(len(data_V)) / fs

    if t_plot_sec is None:
        t_plot_sec = [t_sec[0], t_sec[-1]]

    count = 0
    ax = []
    mean_pD = []

    for Ichan in range(data_V.shape[1]):
        count = count % n_per_page
        if count == 0:
            plt.figure()
            set_figure_tallest_part_wide()

        count += 1

        # Time-domain plot

        # Spectrogram
        plt.subplot(nrow, ncol, Ichan + 1)
        overlap = 1 - 1 / 2
        plots = 0
        f, t, pD = spectrogram(data_V[:, Ichan] * 1e6, fs, nperseg=256, noverlap=int(256 * overlap), mode='psd')
        wT = t + (256 / 2) / fs

        plt.pcolormesh(wT, f, 10 * np.log10(pD))
        plt.gca().invert_yaxis()
        if Ichan > 6:
            plt.xlabel('Time (sec)')
        plt.ylabel('Frequency (Hz)')

        if chan_names is None:
            plt.title('Channel {}'.format(Ichan + 1))
        else:
            plt.title(chan_names[Ichan])

        #plt.clim(+20 + [-35, 0] + 10 * np.log10(256) - 10 * np.log10(256))
        plt.clim(20 + np.array([-35, 0]) + 10 * np.log10(256) - 10 * np.log10(256))
        if f_lim is not None:
            plt.ylim(f_lim)
        plt.xlim(t_plot_sec)

        plt.colorbar(label='Intensity (dB/bin re: 1uV)')
        ax.append(plt.gca())

        if t_mark_sec is not None:
            for Imark in range(t_mark_sec.shape[0]):
                plt.hlines(ymin=plt.ylim()[0], ymax=plt.ylim()[1], x=t_mark_sec[Imark], linestyles='dashed', linewidth=2)

        # Get mean pD within the window
        if t_analyze_sec is not None:
            for Iwin in range(t_analyze_sec.shape[0]):
                K = np.where((wT >= t_analyze_sec[Iwin, 0]) & (wT <= t_analyze_sec[Iwin, 1]))[0]
                mean_pD.append(np.nanmedian(pD[:, K], axis=1))

    # Evaluate cross-channel coherence
    nave = round(4 * (1 / (1 - overlap)))
    plt.subplot(3, 1, 3)
    plots = 1
    f_cohere, coherence_matrix = coherence(data_V[:, 0], data_V[:, 1], fs, nperseg=256, noverlap=int(256 * overlap), nfft=256)
    ############################################################################################
    #coherence_matrix = coherence_matrix.reshape((len(f_cohere), len(t)))
    #coherence_matrix = coherence_matrix.reshape((len(f_cohere), len(t)-1))
    coherence_matrix = coherence_matrix.reshape((len(f_cohere), -1))
    coherence_matrix = coherence_matrix[:, :-1]
    #########################################################################################
    plt.pcolormesh(t, f_cohere, coherence_matrix)
    plt.ylim(f_lim)
    plt.xlim(t_plot_sec)
    plt.colorbar(label='Mean Square Coherence')

    if chan_names is None:
        plt.title('EEG Coherence (Chan 1, Chan 2)')
    else:
        plt.title('EEG Coherence ({}, {})'.format(chan_names[0], chan_names[1]))

    plt.xlabel('Time (sec)')

    plt.tight_layout()
    plt.show()
    plt.close('all')

    return mean_pD


def set_figure_tallest_part_wide():
    # Custom function to set figure size
    # Modify the parameters as per your requirement
    fig_height = 12
    fig_width = 8
    plt.rcParams.update({'figure.figsize': (fig_width, fig_height)})