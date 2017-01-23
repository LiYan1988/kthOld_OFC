clc;
close all;
clear;

load paretoArch2New.mat
load paretoArch4New.mat
load paretoArch5New.mat

%%
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch2New(:,3),paretoArch2New(:,4), 'displayname', 'Optimal Arch 2', 'linewidth', 2);
h(2) = plot(paretoArch4New(:,3),paretoArch4New(:,4), 'displayname', 'Optimal Arch 4', 'linewidth', 2);
h(3) = plot(paretoArch5New(:,3),paretoArch5New(:,4), 'displayname', 'Optimal Arch 5', 'linewidth', 2);

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
legend(h(1:3), 'location', 'southwest')

saveas(figure1, 'paretoNew.jpg')
