clc;
close all;
clear;

load paretoArch2Old.mat
load paretoArch4Old.mat
load paretoArch5Old2.mat

figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch5Old2(:,1),paretoArch5Old2(:,2), '--', ...
    'displayname', 'Optimal trade-off for Arch 3', 'linewidth', 2, 'color', [.93, .69, .13]);

text(paretoArch5Old2(1, 1),paretoArch5Old2(1, 2),'\beta=0', ...
    'fontsize', 14, 'horizontalalignment', 'right')
text(paretoArch5Old2(end, 1),paretoArch5Old2(end, 2),...
    '\beta=100', 'fontsize', 14,'horizontalalignment', 'left',...
    'verticalalignment', 'top')

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput (Tbps)', 'fontsize', 16)
h = legend(h(1), 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'paretoArchitectures.jpg')
