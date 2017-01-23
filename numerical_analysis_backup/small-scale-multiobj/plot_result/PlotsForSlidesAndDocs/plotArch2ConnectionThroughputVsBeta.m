clc;
close all;
clear;

load paretoArch2Old.mat

%%
figure2 = figure('units','normalized','Position', [0.6 0.4 0.35 0.3]);
axes2 = axes('parent', figure2);

yyaxis(axes2, 'left')
h(1) = semilogx(paretoArch2Old(:,5), paretoArch2Old(:,1), 'linewidth', 2, ...
    'displayname', 'throughput, bound');
hold(axes2, 'on')
h(2) = semilogx(paretoArch2Old(:,5), paretoArch2Old(:,3), 'linewidth', 2, ...
    'displayname', 'throughput, heuristic');
ylabel('Throughput (Tbps)', 'fontsize', 16)

yyaxis(axes2, 'right')
h(3) = semilogx(paretoArch2Old(:,5), paretoArch2Old(:,2), 'linewidth', 2, ...
    'displayname', 'connection, bound');
hold(axes2, 'on')
h(4) = semilogx(paretoArch2Old(:,5), paretoArch2Old(:,4), 'linewidth', 2, ...
    'displayname', 'connection, heuristic');
ylabel('Connections', 'fontsize', 16)
ylim([190, 260])

h(5) = semilogx(0, 0, 'linewidth', 2, 'color', 'k', 'displayname', 'upper bound', 'linestyle', '-');
h(6) = semilogx(0, 0, 'linewidth', 2, 'color', 'k', 'displayname', 'heuristic', 'linestyle', '--');

box(axes2, 'on')
grid(axes2, 'on')
xlabel('\beta', 'fontsize', 16)

h = legend(h(5:6), 'location', 'east');
h.FontSize = 12;
saveas(figure2, 'Arch2VsBeta.jpg')
