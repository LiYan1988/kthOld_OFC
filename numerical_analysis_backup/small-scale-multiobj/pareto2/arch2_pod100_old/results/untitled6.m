clear;
close all;
clc;

load Arch5New.mat
load Arch5Old.mat
rupcArch5 = [rupcArch5New, rupcArch5Old];
% rupcArch2 = [rupcArch2(:,1),rupcArch2(:,3),rupcArch2(:,2),rupcArch2(:,4)];
uepcArch5 = [uepcArch5New, uepcArch5Old];
% uepcArch2 = [uepcArch2(:,1),uepcArch2(:,3),uepcArch2(:,2),uepcArch2(:,4)];
%% RUPC
figure1 = figure;
axes1 = axes('Parent', figure1);
hold(axes1, 'on');
box(axes1, 'on');
grid(axes1, 'on');
set(axes1, 'ytick', [0, 0.2, 0.4, 0.6, 0.8, 1]);
pct = [cellstr(num2str(get(axes1, 'ytick')'*100))];
pct = [char(pct), char(ones(size(pct,1),1)*'%')];
set(axes1, 'yticklabel', pct);
set(axes1, 'xtick', [1, 2, 3]);
set(axes1, 'xticklabel', [0, 0.04, 1]);
xlabel('\beta', 'fontsize', 12)
ylabel('Resource utilization', 'fontsize', 12)
bar1 = bar(rupcArch5);
bar1(1).FaceColor = [0.85, 0.33, 0.1];
bar1(2).FaceColor = [0, 0.45, 0.74];
bar1(3).FaceColor = [0.93, 0.69, 0.13];
bar1(4).FaceColor = [0.49, 0.67, 0.19];
set(bar1(3), 'displayname', 'Heuristic, discrete traffic profile')
set(bar1(1), 'displayname', 'Heuristic, smooth traffic profile')
set(bar1(4), 'displayname', 'MILP, discrete traffic profile')
set(bar1(2), 'displayname', 'MILP, smooth traffic profile')
h = legend(axes1, 'show', 'location', 'southwest');
h.FontSize = 12;
saveas(figure1, 'RUPCArch5.jpg')

%% UEPC
figure2 = figure;
axes2 = axes('Parent', figure2);
hold(axes2, 'on');
box(axes2, 'on');
grid(axes2, 'on');
% set(axes2, 'ytick', [0, 0.2, 0.4, 0.6, 0.8, 1]);
% pct = [cellstr(num2str(get(axes1, 'ytick')'*100))];
% pct = [char(pct), char(ones(size(pct,1),1)*'%')];
% set(axes1, 'yticklabel', pct);
set(axes2, 'xtick', [1, 2, 3]);
set(axes2, 'xticklabel', [0, 0.04, 1]);
xlabel('\beta', 'fontsize', 12)
ylabel('Utilization Entropy', 'fontsize', 12)
bar2 = bar(uepcArch5);
bar2(1).FaceColor = [0.85, 0.33, 0.1];
bar2(2).FaceColor = [0, 0.45, 0.74];
bar2(3).FaceColor = [0.93, 0.69, 0.13];
bar2(4).FaceColor = [0.47, 0.67, 0.19];
set(bar2(3), 'displayname', 'Heuristic, discrete traffic profile')
set(bar2(1), 'displayname', 'Heuristic, smooth traffic profile')
set(bar2(4), 'displayname', 'MILP, discrete traffic profile')
set(bar2(2), 'displayname', 'MILP, smooth traffic profile')
h = legend(axes2, 'show', 'location', 'southwest');
h.FontSize = 12;
saveas(figure2, 'UEPCArch5.jpg')