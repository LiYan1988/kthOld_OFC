clc;
close all;
clear;

%% Plot G0
load arch4Guard0.mat
load arch2Guard0.mat
corev = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];

figure2 = figure('unit', 'normalized', 'position', [0.6, 0.6, 0.4, 0.3]);
axes2 = axes('Parent', figure2);
box(axes2, 'on')
hold(axes2, 'on')
grid(axes2, 'on')


h(1) = plot(corev,cnkUbA2G0, '--', 'marker', '^', ...
    'displayname', 'A2 G0 UB Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(2) = plot(corev,cnkHeA2G0, 'marker', '^', ...
    'displayname', 'A2 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);

h(3) = plot(corev,cnkUbA4G0, '--', 'marker', '^', ...
    'displayname', 'A3 G0 UB Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(4) = plot(corev,cnkHeA4G0, 'marker', '^', ...
    'displayname', 'A3 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);

h(5) = plot(corev, cnkUbA2G0, '--', 'marker', '^', ...
    'displayname', 'A4 G0 UB Cnk', 'linewidth', 1.5, ...
    'color', [.93, .69, .13]);

%% G1
load arch4Guard1.mat
load arch2Guard1.mat
load arch5Guard1beta0.mat
corev = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
core2 = [2, 4, 6, 8, 10, 12, 14, 16];

h(6) = plot(corev,cnkUbA2G1, '--', 'marker', 'o', ...
    'displayname', 'A2 G1 UB Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(7) = plot(corev,cnkHeA2G1, 'marker', 'o', ...
    'displayname', 'A2 G1 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);

h(8) = plot(corev,cnkUbA4G1, '--', 'marker', 'o', ...
    'displayname', 'A3 G1 UB Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(9) = plot(corev,cnkHeA4G1, 'marker', 'o', ...
    'displayname', 'A3 G1 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);


h(10) = plot([1, core2], [cnkUbA2G1(1); cnkUbA5G1], '--', 'marker', 'o', ...
    'displayname', 'A4 G1 UB Cnk', 'linewidth', 1.5, ...
    'color', [.93, .69, .13]);

%% G2
load arch4Guard2.mat
load arch2Guard2.mat
corev = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
core2 = [2, 4, 6, 8, 10, 12, 14, 16];

h(11) = plot(corev,cnkUbA2G2, '--', 'marker', 's', ...
    'displayname', 'A2 G2 UB Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(12) = plot(corev,cnkHeA2G2, 'marker', 's', ...
    'displayname', 'A2 G2 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);

h(13) = plot(corev,cnkUbA4G2, '--', 'marker', 's', ...
    'displayname', 'A3 G2 UB Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(14) = plot(corev,cnkHeA4G2, 'marker', 's', ...
    'displayname', 'A3 G2 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);

h(15) = plot(corev, cnkUbA2G2, '--', 'marker', 's', ...
    'displayname', 'A4 G2 UB Cnk', 'linewidth', 1.5, ...
    'color', [.93, .69, .13]);

legend(h(1:end), 'location', 'eastoutside')
xlabel('Number of cores')
ylabel('Connection blocking')
xlim([1, 20])
ytick = get(axes2, 'ytick');
set(axes2, 'ytick', ytick(1:2:end));
set(axes2, 'yticklabel', {'0','20%','40%','60%','80%','100%'});
saveas(figure2, 'cnk.jpg')