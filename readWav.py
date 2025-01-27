import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

folder_path = r'D:/OneDrive - Macau University of Science and Technology/Desktop/MUST_year4A/FYP/concentration/WAVs'

# 获取文件夹中的所有 WAV 文件
file_list = [f for f in os.listdir(folder_path) if f.endswith('.wav')]

# 逐个读取 WAV 文件并绘制波形图
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    sample_rate, data = wavfile.read(file_path)
    
    # 创建时间轴
    time = np.arange(len(data)) / sample_rate
    
    # 绘制波形图
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('EEG Signal')
    plt.show()