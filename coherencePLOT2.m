%% Perform Coherence Analysis

% Define parameters
window = hamming(Nfft);
overlap = Nfft/2;
noverlap = Nfft - overlap;
compare_chan = [2 1;
    ];

%% Calculate spectrogram for each channel pair
coherence = zeros(Nfft/2+1, size(compare_chan, 1));
frequencies = (0:Nfft/2) * (fs/Nfft);
for i = 1:size(compare_chan, 1)
    channel1 = compare_chan(i, 1);
    channel2 = compare_chan(i, 2);
    
    [S, F, T] = spectrogram(data_V(:, channel1), window, noverlap, Nfft, fs);
    spectrogram1 = abs(S);
    
    [S, F, T] = spectrogram(data_V(:, channel2), window, noverlap, Nfft, fs);
    spectrogram2 = abs(S);
    
    % Calculate coherence
    [Cxy, F] = mscohere(data_V(:, channel1), data_V(:, channel2), window, noverlap, Nfft, fs);
    coherence(:, i) = Cxy;
    
    % Plot spectrogram
    figure;
    imagesc(T, F, 10*log10(spectrogram1), [-200 50]);
    set(gca, 'YDir', 'normal');
    colormap hot;
    colorbar;
    title(['Spectrogram Channel ' num2str(channel1)]);
    xlabel('Time (s)');
    ylabel('Frequency (Hz)');
    
    figure;
    imagesc(T, F, 10*log10(spectrogram2), [-200 50]);
    set(gca, 'YDir', 'normal');
    colormap hot;
    colorbar;
    title(['Spectrogram Channel ' num2str(channel2)]);
    xlabel('Time (s)');
    ylabel('Frequency (Hz)');
    
    % Plot coherence
    figure;
    plot(F, coherence(:, i));
    title(['Coherence between Channel ' num2str(channel1) ' and Channel ' num2str(channel2)]);
    xlabel('Frequency (Hz)');
    ylabel('Coherence');
end