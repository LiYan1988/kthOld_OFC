clc;
close all;
clear;

load paretoArch5Old2.mat
paretoArch5Old = paretoArch5Old2;
x=[paretoArch5Old(2:end, 5); 0.2; 0.4; 0.8; 1; 2; 4; 8; 10]*200;
y1=[paretoArch5Old2(2:end, 2); paretoArch5Old2(end, 2)*ones(8, 1)];
y2=[paretoArch5Old2(2:end, 4); paretoArch5Old2(end, 4)*ones(8, 1)];
y3=[paretoArch5Old2(2:end, 1); paretoArch5Old2(end, 1)*ones(8, 1)];
y4=[paretoArch5Old2(2:end, 3); paretoArch5Old2(end, 3)*ones(8, 1)];

%%
figure2 = figure('units','normalized','Position', [0.6 0.4 0.35 0.3]);
axes2 = axes('parent', figure2);

yyaxis(axes2, 'left')
h(1) = semilogx(x, y3, 'linewidth', 2, ...
    'displayname', 'throughput, bound');
hold(axes2, 'on')
h(2) = semilogx(x, y4, 'linewidth', 2, ...
    'displayname', 'throughput, heuristic');
ylabel('Throughput (Tbps)', 'fontsize', 16)

yyaxis(axes2, 'right')
h(3) = semilogx(x, y1, 'linewidth', 2, ...
    'displayname', 'connection, bound');
hold(axes2, 'on')
h(4) = semilogx(x, y2, 'linewidth', 2, ...
    'displayname', 'connection, heuristic');
ylabel('Connections', 'fontsize', 16)
ylim([200, 260])
xlim([200*1e-5, 200*1e1])

h(5) = semilogx(0, 0, 'linewidth', 2, 'color', 'k', 'displayname', 'upper bound', 'linestyle', '-');
h(6) = semilogx(0, 0, 'linewidth', 2, 'color', 'k', 'displayname', 'heuristic', 'linestyle', '--');

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)

h = legend(h(5:6), 'location', 'east');
h.FontSize = 12;
saveas(figure2, 'Arch5VsBeta.jpg')
