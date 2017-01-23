clc;
close all;
clear;

load paretoArch2Old.mat
load paretoArch4Old.mat
load paretoArch5Old2.mat

figure1 = figure('units','normalized','Position', [0.1 0.1 0.35 0.3]);
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')

h(1) = plot(paretoArch2Old(:,1),paretoArch2Old(:,2), ':', ...
    'displayname', 'A1, upper bound', 'linewidth', 3, 'color', [.93, .69, .13]);
x = paretoArch2Old(:,3);
y = paretoArch2Old(:,4);
y0 = smooth(x, y);
h(2) = plot(x,y0, ...
    'displayname', 'A1, heuristic', 'linewidth', 3, 'color', [.93, .69, .13]);

h(3) = plot(paretoArch4Old(:,1),paretoArch4Old(:,2), ':', ...
    'displayname', 'A2, upper bound', 'linewidth', 3, 'color', [0.85, 0.33, 0.1]);
h(4) = plot(paretoArch4Old(7:end,3),paretoArch4Old(7:end,4), ...
    'displayname', 'A2, heuristic', 'linewidth', 3, 'color', [0.85, 0.33, 0.1]);

h(5) = plot(paretoArch5Old2(:,1),paretoArch5Old2(:,2), ':', ...
    'displayname', 'A3, upper bound', 'linewidth', 3, 'color', [0, 0.45, 0.74]);
x = paretoArch5Old2(:,3);
x(11) = [];
y = paretoArch5Old2(:,4);
y(11) = [];
y0 = smooth(x, y,7);
h(6) = plot(x(8:end),y0(8:end), ...
    'displayname', 'A3, heuristic', 'linewidth', 3, 'color', [0, 0.45, 0.74]);

xlabel('Number of Connections', 'fontsize', 18)
ylabel('Throughput Tbps', 'fontsize', 18)
% h = legend(h(1:6), 'location', 'southwest');
% h.FontSize = 18;
set(axes1, 'linewidth', 1)
set(axes1, 'gridalpha', 0.5)
set(axes1, 'FontSize', 14)
saveas(figure1, 'paretoArchitectures.jpg')
