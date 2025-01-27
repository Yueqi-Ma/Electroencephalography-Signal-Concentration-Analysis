import numpy as np
import matplotlib.pyplot as plt

def plot_data_time_domain(data_V, fs, n_per_page=8, nrow=4, ncol=2):
    t_sec = np.arange(data_V.shape[0]) / fs  # 计算时间轴（单位：秒）
    n_channels = data_V.shape[1]  # 数据通道数
    n_plots = min(n_per_page, n_channels)  # 每页绘制的子图数

    fig, axs = plt.subplots(nrow, ncol, figsize=(12, 10))  # 创建子图布局
    fig.tight_layout(pad=3.0)  # 调整子图之间的间距

    for i in range(n_plots):
        ax = axs.flat[i] if n_plots > 1 else axs  # 多个子图时，使用平坦索引
        ax.plot(t_sec, data_V[:, i])
        ax.set_title(f"Channel {i+1}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

    # 如果通道数超过每页绘制的子图数，则创建多页
    if n_channels > n_per_page:
        n_pages = int(np.ceil(n_channels / n_per_page))
        for page in range(1, n_pages):
            fig, axs = plt.subplots(nrow, ncol, figsize=(12, 10))
            fig.tight_layout(pad=3.0)

            for i in range(n_per_page):
                channel_idx = page * n_per_page + i
                if channel_idx < n_channels:
                    ax = axs.flat[i] if n_per_page > 1 else axs
                    ax.plot(t_sec, data_V[:, channel_idx])
                    ax.set_title(f"Channel {channel_idx+1}")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("Amplitude")

    plt.show()