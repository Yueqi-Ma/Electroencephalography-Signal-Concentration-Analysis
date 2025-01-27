

addpath('functions\');

%pname = 'SaveData_ProcessingGUI\';
% fname = 'openBCI_raw_2013-11-11_13-55-54.txt'; %dummy data...8-channels
% fname = 'openBCI_raw_2013-11-14_16-13-26.txt';  %dummy data...16-channels
%fname = 'openBCI_raw_2013-12-24_13-53-54_rxc_relaxation.txt'; t_closed_sec = [125 350];sname='Relaxing';
%fname = 'openBCI_raw_2013-12-24_13-26-11_rxc_meditation.txt'; t_closed_sec = [350 1050];sname='Meditating';
%scale_fac_volts_count=2.23e-8;

Nfft = 256; f_lim = [0 100];
pname = 'SavedData\';
t_mark_sec = [];mark_names={};
t_plot_sec=[];
chan_names={};
switch 20
    case 10
        %here, elec1 was on left forehead and elec2 was on back of head
        %ref on left ear lob
        pname = '..\2014-04-05 Impedance and Concentration\SavedData\';
        fname = '10-openBCI_raw_2014-04-19_10-23-36_EyesClosed_8secBreaths.txt';
        if (1)
            t_sig_sec = [285 336];
            t_baseline_sec = [187 213];
        else
            t_sig_sec = [215 285];
            t_baseline_sec = [345 400];
        end
        t_mark_sec = [t_sig_sec;t_baseline_sec];
    case 12
        %here, elec1 was on left forehead and elec2 was on back of head
        %ref on left ear lob
        pname = '..\2014-04-05 Impedance and Concentration\SavedData\';
        fname = '12-openBCI_raw_2014-04-19_10-40-38_countbackwardsby3.txt';
        t_sig_sec = [90 130];
        %t_baseline_sec = [40 55];
        t_baseline_sec = [155 179];
        t_mark_sec = [40 55; t_sig_sec;t_baseline_sec];
        mark_names = {'Eyes Closed';'Count Back by 3';'Eyes Closed'};
    case 13
        %here, elec1 was on left forehead and elec2 was on right forehead.
        %ref on left ear lobe
        pname = '..\2014-04-05 Impedance and Concentration\SavedData\';
        fname = '13-openBCI_raw_2014-04-19_10-54-51_bothOnForehead_countback.txt';
        %t_sig_sec = [63 84];
        t_sig_sec = [100 113];
        %t_baseline_sec = [47 55];
        t_baseline_sec = [65 80];
        t_mark_sec = [47 55; t_sig_sec;t_baseline_sec];
        mark_names = {'Eyes Closed';'Count Back by 3';'Eyes Closed'};
        t_analyze_sec = t_mark_sec;
    case 20
        %here, elec1 was on left forehead and elec2 was on right forehead.
        %ref on left ear lobe
        fname = 'openBCI_raw_2014-04-23_06-52-48_Breakfast_Birds_CountBack.mat';
        sname = '2014-04-23 Breakfast, Web, Birds, Concentration';
        chan_names = {'Left Forehead';'Right Forehead'};
        t_mark_sec = [17*60+43 21*60+31 26*60+41-5  29*60+23 31*60+2];
        t_mark_sec = [t_mark_sec(1:end-1)' t_mark_sec(2:end)'];
        mark_names = {'Gaze Outside','Internet','Eyes Closed','Count Back by 3'};
        if 1
            t_mark_sec = [719 967;t_mark_sec];
            mark_names = {'Internet',mark_names};
        end
        t_plot_sec = [680 1890];
end
t_analyze_sec = t_mark_sec;
N = Nfft;
t_lim_sec = [];
if ~isempty(t_mark_sec)
    t_lim_sec = [t_mark_sec(1) t_mark_sec(end)];
end


compare_chan = [2 1;
    ];


%% load data
data_uV = load([pname fname]);  %loads data as microvolts
if isstruct(data_uV);data_uV = data_uV.data_uV;end;
%fs = data2.fs_Hz;
fs = 250;
count = data_uV(:,1);  %first column is a packet counter (though it's broken)
data_V = data_uV(:,2:end) * 1e-6; %other columns are data
clear data_uV;

data_V = data_V(:,1:2);  %keep just these channels

%% filter data
%data_V = data_V - ones(size(data_V,1),1)*mean(data_V);
[b,a]=butter(2,[1 100]/(fs/2));
data_V = filter(b,a,data_V);


%% analyze data
mean_data_V = mean(data_V);
median_data_V = median(data_V);
std_data_V = std(data_V);
%spread_data_V = diff(xpercentile(data_V,0.5+(0.68-0.5)*[-1 1]))/2;
spread_data_V = diff(prctile(data_V,0.5+(0.68-0.5)*[0 100]))/2;%%%%%%%%%%%%
spread_data_V = median(spread_data_V)*ones(size(spread_data_V));



% Perform Coherence Analysis

% Define parameters
window = hamming(Nfft);
overlap = Nfft/2;
noverlap = Nfft - overlap;
compare_chan = [2 1];

% Calculate coherence for each channel pair
coherence_vals = zeros(Nfft/2+1, size(compare_chan, 1));
frequencies = (0:Nfft/2) * (fs/Nfft);
for i = 1:size(compare_chan, 1)
    channel1 = compare_chan(i, 1);
    channel2 = compare_chan(i, 2);
    
    [S, F, T] = spectrogram(data_V(:, channel1), window, noverlap, Nfft, fs);
    spectrogram1 = abs(S);
    
    [S, F, T] = spectrogram(data_V(:, channel2), window, noverlap, Nfft, fs);
    spectrogram2 = abs(S);
    
    % Calculate coherence
    fftx = fft(data_V(:, channel1));
    ffty = fft(data_V(:, channel2));
    nave = 10; % Set the value of nave
    
    [coherence, ~, ~] = calcCoherence(fftx, ffty, nave);
    
    coherence_vals(:, i) = coherence;
end

% Plot coherence values vs frequency for each channel pair
figure;
hold on;
for i = 1:size(compare_chan, 1)
    channel1 = compare_chan(i, 1);
    channel2 = compare_chan(i, 2);
    
    plot(frequencies, coherence_vals(:, i), 'LineWidth', 2);
end
hold off;
xlabel('Frequency (Hz)');
ylabel('Coherence');
legend('Channel 1 vs Channel 2', 'Channel 3 vs Channel 4', 'Channel 5 vs Channel 6');
title('Coherence vs Frequency');






