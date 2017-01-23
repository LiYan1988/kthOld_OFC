clc;
clear;
close all;

npods = [100,150,200];

% arch1
arch1 = [150, 225, 300];
% figure(1); 
% bar(npods,arch1)

load pod100_final.csv
load pod150_final.csv
load pod200_final.csv

% arch2

arch2 = [pod100_final(:,1)';pod150_final(:,1)';pod200_final(:,1)'];
num = '(a)';
createfigure3(npods,arch2,num)

% arch4
arch4 = [pod100_final(:,2)';pod150_final(:,2)';pod200_final(:,2)'];
num = '(b)';
createfigure3(npods,arch4,num)

% arch5
arch5 = [pod100_final(:,3)';pod150_final(:,3)';pod200_final(:,3)'];
num = '(c)';
createfigure3(npods,arch5,num)