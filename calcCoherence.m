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
% ����һ����Ϊ `calcCoherence` �ĺ��������ڼ����źŵ�����ԡ�
% 
% ���������������������
% - `fftx`����ʾ�ź�1����ɢ����Ҷ�任�����
% - `ffty`����ʾ�ź�2����ɢ����Ҷ�任�����
% - `nave`����ʾƽ���Ŀ�����
% 
% ���������������
% - `coherence`����ʾ����õ�������Խ����
% - `yx_raw`����ʾ�ź�1���ź�2��ֱ�ӳ˻���
% - `yx_filt`����ʾ�� `yx_raw` ����ƽ���˲���Ľ����
% 
% �����Ǻ����Ĵ�����ͣ�
% 
% ���ȣ����������ź�1���ź�2������غ������ֱ𱣴��� `xx` �� `yy` �С�����غ������ź���������ĸ�������ˡ�

% Ȼ�󣬺��������ź�1���ź�2�Ļ���غ����������� `yx_raw` �С�����غ������ź�1�ĸ��������ź�2�ĳ˻���
% 
% �����������붨��һ�� `nave` ���ȵ��ƶ�ƽ���˲���ϵ�� `b`�����ڶ� `yx_raw`��`xx` �� `yy` �����˲���
% 
% Ȼ�󣬺���ʹ�� `filter` ������ `yx_raw`��`xx` �� `yy` �����˲��������õ��˲���Ľ�� `yx_filt`��`xx` �� `yy`��
% 
% ��󣬺������������ `coherence`��ͨ�����˲���� `yx_filt` �ľ���ֵ��ƽ������ `xx` �� `yy` �ĳ˻��õ���
% 
% ��Ҫע����ǣ��ú������źŽ�����ƽ���˲��������Լ���ź��ڿ����֮�������Ա仯������Եļ�������˲���Ľ����������ԭʼ�� `yx_raw`��
% 

