clc;
clear;
% close all;

load data_core_ave.mat
% save data_core_ave.mat
%% established connections
% u = [125*(1:20)',cnk_ave(:,1:9)];
% createfigure1(u);

%% blocking probability
% u = [125*(1:20)',cnk_ave(:,1:9)];
% for i=1:10
%     u(:,i) = (cnk_ave(:,10)-u(:,i))./cnk_ave(:,10);
% end
createfigure2(u);