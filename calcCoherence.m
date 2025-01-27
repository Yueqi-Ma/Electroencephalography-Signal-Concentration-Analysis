% %%
function [coherence,yx_raw,yx_filt]=calcCoherence(fftx,ffty,nave)

xx = fftx.*conj(fftx);
yy = ffty.*conj(ffty);
yx_raw = conj(fftx).*(ffty);
%coherence = ((abs(yx)).^2)./(xx.*yy);  %this always returns 1.0...can't be right

%ahh, need averaging to see if movement from block to block coherent
b = 1/nave*ones(nave,1);  %do a moving average filter over nave blocks
yx_filt = filter(b,1,yx_raw')';  %must filter before the ABS operation (the ABS is later)
xx = filter(b,1,xx')';
yy = filter(b,1,yy')';
coherence = (abs(yx_filt).^2)./ (xx.*yy);  






%%
% function [coherence, yx_raw, yx_filt] = calcCoherence(fftx, ffty, nave)
%     xx = fftx .* conj(fftx);
%     yy = ffty .* conj(ffty);
%     yx_raw = conj(fftx) .* ffty;
% 
%     b = 1/nave * ones(nave, 1);
%     yx_filt = filter(b, 1, yx_raw')';
% 
%     coherence = (abs(yx_filt).^2) ./ (filter(b, 1, xx')' .* filter(b, 1, yy')');
% end



% Basic Form: http://ocw.mit.edu/courses/earth-atmospheric-and-planetary-sciences/12-864-inference-from-data-and-models-spring-2005/lecture-notes/tsamsfmt_1_18.pdf
% Add Averaging: http://www.dsprelated.com/dspbooks/mdft/Coherence_Function.html
% Mostly worthless: http://en.wikipedia.org/wiki/Coherence_(signal_processing)

%%
% 这是一个名为 `calcCoherence` 的函数，用于计算信号的相干性。
% 
% 函数接受三个输入参数：
% - `fftx`：表示信号1的离散傅里叶变换结果。
% - `ffty`：表示信号2的离散傅里叶变换结果。
% - `nave`：表示平均的块数。
% 
% 函数的输出包括：
% - `coherence`：表示计算得到的相干性结果。
% - `yx_raw`：表示信号1和信号2的直接乘积。
% - `yx_filt`：表示对 `yx_raw` 进行平均滤波后的结果。
% 
% 下面是函数的代码解释：
% 
% 首先，函数计算信号1和信号2的自相关函数，分别保存在 `xx` 和 `yy` 中。自相关函数是信号与其自身的复共轭相乘。

% 然后，函数计算信号1和信号2的互相关函数，保存在 `yx_raw` 中。互相关函数是信号1的复共轭与信号2的乘积。
% 
% 接下来，代码定义一个 `nave` 长度的移动平均滤波器系数 `b`，用于对 `yx_raw`、`xx` 和 `yy` 进行滤波。
% 
% 然后，函数使用 `filter` 函数对 `yx_raw`、`xx` 和 `yy` 进行滤波操作，得到滤波后的结果 `yx_filt`、`xx` 和 `yy`。
% 
% 最后，函数计算相干性 `coherence`，通过将滤波后的 `yx_filt` 的绝对值的平方除以 `xx` 和 `yy` 的乘积得到。
% 
% 需要注意的是，该函数对信号进行了平均滤波操作，以检测信号在块与块之间的相干性变化。相干性的计算采用滤波后的结果，而不是原始的 `yx_raw`。
% 

