clc;
clear;
% close all;

load data_pod_ave.mat
% save data_pod_ave.mat

createfigure(data_ave(:,12), data_ave(:,1:10))