% 导入信号处理工具箱
import matlab.signal.*

% 定义凯泽窗参数
windowLength = Nfft;
beta = 10;
window = kaiser(windowLength, beta);

% ...

% 使用凯泽窗计算频谱图
[S, F, T] = spectrogram(data_V(:, channel1), window, noverlap, Nfft, fs);
spectrogram1 = abs(S);

[S, F, T] = spectrogram(data_V(:, channel2), window, noverlap, Nfft, fs);
spectrogram2 = abs(S);

% ...

% 绘制频谱图
figure;
subplot(2, 1, 1);
imagesc(T, F, 10*log10(spectrogram1), [-200 50]);
set(gca, 'YDir', 'normal');
colormap hot;
colorbar;
title(['Spectrogram Channel ' num2str(channel1)]);
xlabel('Time (s)');
ylabel('Frequency (Hz)');

subplot(2, 1, 2);
imagesc(T, F, 10*log10(spectrogram2), [-200 50]);
set(gca, 'YDir', 'normal');
colormap hot;
colorbar;
title(['Spectrogram Channel ' num2str(channel2)]);
xlabel('Time (s)');
ylabel('Frequency (Hz)');

% ...