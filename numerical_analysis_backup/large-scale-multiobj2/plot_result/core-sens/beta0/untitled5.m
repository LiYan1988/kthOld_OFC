clc;
close all;
clear;

load arch4Guard2.mat
load arch4Guard1.mat
load arch4Guard0.mat
load arch2Guard2.mat
load arch2Guard1.mat
load arch2Guard0.mat
corev = [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20];
%% Plot connections
% colors: [0, 0.45, 0.74], [.85, .33, .1], [.93, .69, .13]
figure1 = figure;
axes1 = axes('Parent', figure1);
box(axes1, 'on')
hold(axes1, 'on')
grid(axes1, 'on')
h(1) = plot(corev,thpUbA4G2, '--', ...
    'displayname', 'A4 G2 Opt Th', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(2) = plot(corev,thpHeA4G2, ...
    'displayname', 'A4 G2 Heu Th', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(3) = plot(corev,thpUbA4G1, '--', ...
    'displayname', 'A4 G1 Opt Th', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(4) = plot(corev,thpHeA4G1, ...
    'displayname', 'A4 G1 Heu Th', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(5) = plot(corev,thpUbA4G0, '--', ...
    'displayname', 'A4 G0 Opt Th', 'linewidth', 2, ...
    'color', [.93, .69, .13]);
h(6) = plot(corev,thpHeA4G0, ...
    'displayname', 'A4 G0 Heu Th', 'linewidth', 2, ...
    'color', [.93, .69, .13]);

h(7) = plot(corev,thpUbA2G2, '--', 'marker', '^', ...
    'displayname', 'A2 G2 Opt Th', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(8) = plot(corev,thpHeA2G2, 'marker', '^', ...
    'displayname', 'A2 G2 Heu Th', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(9) = plot(corev,thpUbA2G1, '--', 'marker', '^', ...
    'displayname', 'A2 G1 Opt Th', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(10) = plot(corev,thpHeA2G1, 'marker', '^', ...
    'displayname', 'A2 G1 Heu Th', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(11) = plot(corev,thpUbA2G0, '--', 'marker', '^', ...
    'displayname', 'A2 G0 Opt Th', 'linewidth', 2, ...
    'color', [.93, .69, .13]);
h(12) = plot(corev,thpHeA2G0, 'marker', '^', ...
    'displayname', 'A2 G0 Heu Th', 'linewidth', 2, ...
    'color', [.93, .69, .13]);

legend(h(1:end), 'location', 'southwest')
xlabel('Number of cores')
ylabel('Throughput blocking')
xlim([1, 20])
ytick = get(axes1, 'ytick');
set(axes1, 'ytick', ytick(1:2:end));
set(axes1, 'yticklabel', {'0','20%','40%','60%','80%','100%'});

%% Plot throughput
figure2 = figure;
axes2 = axes('Parent', figure2);
box(axes2, 'on')
hold(axes2, 'on')
grid(axes2, 'on')
h(1) = plot(corev,cnkUbA4G2, '--', ...
    'displayname', 'A4 G2 Opt Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(2) = plot(corev,cnkHeA4G2, ...
    'displayname', 'A4 G2 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(3) = plot(corev,cnkUbA4G1, '--', ...
    'displayname', 'A4 G1 Opt Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(4) = plot(corev,cnkHeA4G1, ...
    'displayname', 'A4 G1 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(5) = plot(corev,cnkUbA4G0, '--', ...
    'displayname', 'A4 G0 Opt Cnk', 'linewidth', 2, ...
    'color', [.93, .69, .13]);
h(6) = plot(corev,cnkHeA4G0, ...
    'displayname', 'A4 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [.93, .69, .13]);

h(7) = plot(corev,cnkUbA2G2, '--', 'marker', '^', ...
    'displayname', 'A2 G2 Opt Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(8) = plot(corev,cnkHeA2G2, 'marker', '^', ...
    'displayname', 'A2 G2 Heu Cnk', 'linewidth', 2, ...
    'color', [0, 0.45, 0.74]);
h(9) = plot(corev,cnkUbA2G1, '--', 'marker', '^', ...
    'displayname', 'A2 G1 Opt Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(10) = plot(corev,cnkHeA2G1, 'marker', '^', ...
    'displayname', 'A2 G1 Heu Cnk', 'linewidth', 2, ...
    'color', [.85, .33, .1]);
h(11) = plot(corev,cnkUbA2G0, '--', 'marker', '^', ...
    'displayname', 'A2 G0 Opt Cnk', 'linewidth', 2, ...
    'color', [.93, .69, .13]);
h(12) = plot(corev,cnkHeA2G0, 'marker', '^', ...
    'displayname', 'A2 G0 Heu Cnk', 'linewidth', 2, ...
    'color', [.93, .69, .13]);

legend(h(1:6), 'location', 'southwest')
xlabel('Number of cores')
ylabel('Connection blocking')
xlim([1, 20])
ytick = get(axes2, 'ytick');
set(axes2, 'ytick', ytick(1:2:end));
set(axes2, 'yticklabel', {'0','20%','40%','60%','80%','100%'});