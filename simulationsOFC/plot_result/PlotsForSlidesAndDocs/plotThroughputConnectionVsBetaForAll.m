clc;
close all;
clear;

load paretoArch2Old.mat

%%
figure2 = figure('units','normalized','Position', [0.6 0.4 0.35 0.3]);
axes2 = axes('parent', figure2);
h(1) = semilogx(paretoArch2Old(:,5)*200, paretoArch2Old(:,4), 'linewidth', 2, ...
    'displayname', 'A1', 'color', [.93, .69, .13]);
ylabel('Throughput (Tbps)', 'fontsize', 16)

hold(axes2, 'on')
%%
load paretoArch4Old.mat
h(2) = semilogx(paretoArch4Old(:,5)*200, paretoArch4Old(:,4), 'linewidth', 2, ...
    'displayname', 'A2', 'color', [0.85, 0.33, 0.1]);

%%
load paretoArch5Old2.mat
paretoArch5Old = paretoArch5Old2;
x=[paretoArch5Old(2:end, 5); 0.2; 0.4; 0.8; 1; 2; 4; 8; 10]*200;
y1=[paretoArch5Old2(2:end, 2); paretoArch5Old2(end, 2)*ones(8, 1)];
y2=[paretoArch5Old2(2:end, 4); paretoArch5Old2(end, 4)*ones(8, 1)];
y3=[paretoArch5Old2(2:end, 1); paretoArch5Old2(end, 1)*ones(8, 1)];
y4=[paretoArch5Old2(2:end, 3); paretoArch5Old2(end, 3)*ones(8, 1)];

h(3) = semilogx(x, y2, 'linewidth', 2, ...
    'displayname', 'A3', 'color', [0, 0.45, 0.74]);

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)
ylabel('Throughput (Tbps)', 'fontsize', 16)
h = legend(h(1:3), 'location', 'southeast');
h.FontSize = 18;
set(axes2, 'linewidth', 1)
set(axes2, 'gridalpha', 0.5)
set(axes2, 'fontsize', 14)
% set(axes2, 'minorgridalpha', 0.5)
xlim([2e-3, 2e3])

% plot(0.4,paretoArch2Old(11, 4),'marker', 'o', ...
% 'linewidth', 3, 'markersize', 8, 'color', [0.47, 0.67, 0.19])
% 
% plot(0.2,paretoArch4Old(10, 4),'marker', 'o', ...
% 'linewidth', 3, 'markersize', 8, 'color', [0.47, 0.67, 0.19])
% 
% plot(0.8,paretoArch5Old2(12, 4),'marker', 'o', ...
% 'linewidth', 3, 'markersize', 8, 'color', [0.47, 0.67, 0.19])

saveas(figure2, 'ThroughputVsBetaAll.jpg')