import scipy.io
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import coherence

# 加载MATLAB文件
data = scipy.io.loadmat('SavedData/openBCI_raw_2014-04-23_06-52-48_Breakfast_Birds_CountBack.mat')

# 提取两个通道的信号
channel1 = data['channel1']
channel2 = data['channel2']

# 转换为一维数组
channel1 = np.ravel(channel1)
channel2 = np.ravel(channel2)

# 设置采样频率
fs = 1000  # 假设采样频率为1000Hz

# 计算相干性
frequencies, coherence_values = coherence(channel1, channel2, fs=fs)

# 绘制相干性图像
plt.figure()
plt.plot(frequencies, coherence_values)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Coherence')
plt.title('Coherence between Channel 1 and Channel 2')
plt.grid(True)
plt.show()