clc;
clear;
close all;

load data_load_ave1.mat
% save data_load_ave1.mat

a = [data_ave(:,11),data_ave(:,1:9)];
createfigure1(a)
