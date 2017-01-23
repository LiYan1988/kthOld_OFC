clc;
close all;
clear;

load arch5RU.mat
load arch4RU.mat
load arch2RU.mat

betav1 = [0, ...
    1e-5, 2e-5, 4e-5, 8e-5, ...
    1e-4, 2e-4, 4e-4, 8e-4, ...
    1e-3, 2e-3, 4e-3, 8e-3, ...
    1e-2, 2e-2, 4e-2, 8e-2, ...
    1e-1, 2e-1, 4e-1, 1, 10];

betav2 = [0, 1e-5, 2e-5, 4e-5, ...
    8e-5, 1e-4, 2e-4, 4e-4, ...
    8e-4, 1e-3, 2e-3, 4e-3, ...
    8e-3, 1e-2, 2e-2, 4e-2, ...
    8e-2, 1e-1];
ruVsBetaA5(end+1:end+4) = ruVsBetaA5(end);
ueAveVsBetaA5(end+1:end+4) = ueAveVsBetaA5(end);
% figure1 = figure;
% semilogx(betav1, ruVsBetaA2, 'linewidth', 2, 'displayname', 'Arch 2')
% hold on;
% semilogx(betav1, ruVsBetaA4, 'linewidth', 2, 'displayname', 'Arch 4')
% semilogx(betav1, ruVsBetaA5, 'linewidth', 2, 'displayname', 'Arch 5')
% figure;
% semilogx(betav1, efVsBetaA2)
% hold on;
% semilogx(betav1, efVsBetaA4)
% semilogx(betav2, efVsBetaA5)

figure1 = figure;
semilogx(betav1, ueAveVsBetaA2, 'linewidth', 2, 'displayname', 'Arch 2')
hold on;
semilogx(betav1, ueAveVsBetaA4, 'linewidth', 2, 'displayname', 'Arch 4')
semilogx(betav1, ueAveVsBetaA5, 'linewidth', 2, 'displayname', 'Arch 5')