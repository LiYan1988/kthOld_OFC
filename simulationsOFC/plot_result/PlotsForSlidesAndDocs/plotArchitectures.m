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
h(1) = plot(paretoArch4Old(:,1),paretoArch4Old(:,2), ':', ...
    'displayname', 'Arch 3, upper bound', 'linewidth', 2, 'color', [0, 0.45, 0.74]);
h(2) = plot(paretoArch4Old(7:end,3),paretoArch4Old(7:end,4), ...
    'displayname', 'Arch 3, heuristic', 'linewidth', 2, 'color', [0, 0.45, 0.74]);
h(3) = plot(paretoArch2Old(:,1),paretoArch2Old(:,2), ':', ...
    'displayname', 'Arch 2, upper bound', 'linewidth', 2, 'color', [.85, .33, .1]);
x = paretoArch2Old(:,3);
y = paretoArch2Old(:,4);
y0 = smooth(x, y);
h(4) = plot(x,y0, ...
    'displayname', 'Arch 2, heuristic', 'linewidth', 2, 'color', [.85, .33, .1]);


h(5) = plot(paretoArch5Old2(:,1),paretoArch5Old2(:,2), ':', ...
    'displayname', 'Arch 4, upper bound', 'linewidth', 2, 'color', [.93, .69, .13]);
x = paretoArch5Old2(:,3);
x(11) = [];
y = paretoArch5Old2(:,4);
y(11) = [];
y0 = smooth(x, y,7);
h(6) = plot(x(8:end),y0(8:end), ...
    'displayname', 'Arch 4, heuristic', 'linewidth', 2, 'color', [.93, .69, .13]);

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
h = legend(h(1:6), 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'paretoArchitectures.jpg')
