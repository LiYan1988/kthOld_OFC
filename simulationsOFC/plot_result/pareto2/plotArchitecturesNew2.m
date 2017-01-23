clc;
close all;
clear;

load paretoArch4Old.mat
load paretoArch4New.mat

figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch4New(:,1),paretoArch4New(:,2)*0.001, '--', ...
    'displayname', 'Arch 4 New, optimal', 'linewidth', 2, 'color', [0, 0.45, 0.74]);
h(2) = plot(paretoArch4New(:,3),paretoArch4New(:,4)*0.001, ...
    'displayname', 'Arch 4 New, heuristic', 'linewidth', 2, 'color', [0, 0.45, 0.74]);
h(3) = plot(paretoArch4Old(:,1),paretoArch4Old(:,2)*0.001, '--', ...
    'displayname', 'Arch 4 Old, optimal', 'linewidth', 2, 'color', [.85, .33, .1]);
h(4) = plot(paretoArch4Old(:,3),paretoArch4Old(:,4)*0.001, ...
    'displayname', 'Arch 4 Old, heuristic', 'linewidth', 2, 'color', [.85, .33, .1]);

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:4), 'location', 'southwest');
h.FontSize = 12;
% saveas(figure1, 'pareto_arch2.jpg')
