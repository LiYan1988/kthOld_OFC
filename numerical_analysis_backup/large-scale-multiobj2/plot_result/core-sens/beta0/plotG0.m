clc;
close all;
clear;

load arch4Guard0.mat
load arch2Guard0.mat
corev = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];

%% Plot connections
% colors: [0, 0.45, 0.74], [.85, .33, .1], [.93, .69, .13]
% figure1 = figure;
% axes1 = axes('Parent', figure1);
% box(axes1, 'on')
% hold(axes1, 'on')
% grid(axes1, 'on')
% 
% h(1) = plot(corev,thpUbA2G0, '--', ...'marker', '^', ...
%     'displayname', 'A2 G0 UB Th', 'linewidth', 2, ...
%     'color', [.85, .33, .1]);
% h(2) = plot(corev,thpHeA2G0, ...'marker', '^', ...
%     'displayname', 'A2 G0 Heu Th', 'linewidth', 2, ...
%     'color', [.85, .33, .1]);
% 
% h(3) = plot(corev,thpUbA4G0, '--', ...
%     'displayname', 'A3 G0 UB Th', 'linewidth', 2, ...
%     'color', [0, 0.45, 0.74]);
% h(4) = plot(corev,thpHeA4G0, ...
%     'displayname', 'A3 G0 Heu Th', 'linewidth', 2, ...
%     'color', [0, 0.45, 0.74]);
% 
% h(5) = plot(corev, thpUbA2G0, '--', ...'marker', '^', ...
%     'displayname', 'A4 G0 UB Th', 'linewidth', 1.5, ...
%     'color', [.93, .69, .13]);
% 
% legend(h(1:end), 'location', 'northeast')
% xlabel('Number of cores')
% ylabel('Throughput blocking')
% xlim([1, 20])
% ytick = get(axes1, 'ytick');
% set(axes1, 'ytick', ytick(1:2:end));
% set(axes1, 'yticklabel', {'0','20%','40%','60%','80%','100%'});
% saveas(figure1, 'G0thp.jpg')

%% Plot connection
figure2 = figure;
axes2 = axes('Parent', figure2);
box(axes2, 'on')
hold(axes2, 'on')
grid(axes2, 'on')


h(1) = plot(corev,cnkUbA2G0, '--', ...'marker', '^', ...
    'displayname', 'A2 G0 UB Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(2) = plot(corev,cnkHeA2G0, ...'marker', '^', ...
    'displayname', 'A2 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);

h(3) = plot(corev,cnkUbA4G0, '--', ...
    'displayname', 'A3 G0 UB Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(4) = plot(corev,cnkHeA4G0, ...
    'displayname', 'A3 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);

h(5) = plot(corev, cnkUbA2G0, '--', ...'marker', '^', ...
    'displayname', 'A4 G0 UB Cnk', 'linewidth', 1.5, ...
    'color', [.93, .69, .13]);

legend(h(1:end), 'location', 'northeast')
xlabel('Number of cores')
ylabel('Connection blocking')
xlim([1, 20])
ytick = get(axes2, 'ytick');
set(axes2, 'ytick', ytick(1:2:end));
set(axes2, 'yticklabel', {'0','20%','40%','60%','80%','100%'});
saveas(figure2, 'G0cnk.jpg')