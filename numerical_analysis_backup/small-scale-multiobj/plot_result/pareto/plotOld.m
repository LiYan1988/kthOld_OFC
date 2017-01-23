clc;
close all;
clear;

load paretoArch2Old.mat
load paretoArch4Old.mat
load paretoArch5Old.mat

%%
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(paretoArch2Old(:,1),paretoArch2Old(:,2), 'displayname', 'Optimal Arch 2', 'linewidth', 2);
h(2) = plot(paretoArch4Old(:,1),paretoArch4Old(:,2), 'displayname', 'Optimal Arch 4', 'linewidth', 2);
h(3) = plot(paretoArch5Old(1:10,1),paretoArch5Old(1:10,2), 'displayname', 'Optimal Arch 5', 'linewidth', 2);

% h(1) = plot(paretoArch2Old(:,3),paretoArch2Old(:,4), 'displayname', 'Optimal Arch 2', 'linewidth', 2);
% h(2) = plot(paretoArch4Old(:,3),paretoArch4Old(:,4), 'displayname', 'Optimal Arch 4', 'linewidth', 2);
% h(3) = plot(paretoArch5Old(:,3),paretoArch5Old(:,4), 'displayname', 'Optimal Arch 5', 'linewidth', 2);

xlabel('Number of Connections', 'fontsize', 16)
ylabel('Throughput Tbps', 'fontsize', 16)
legend(h(1:3), 'location', 'southwest')

saveas(figure1, 'paretoOld.jpg')
