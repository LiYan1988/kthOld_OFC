clc;
close all;
clear;

Nele = 0.15;
Tele = 0.85;
% f = [-1, zeros(1, 3), -1, -1];
f = -ones(1, 6);
% f = [1, zeros(1, 5)];
% f = zeros(1, 6);
x = trafficProfile(f, Nele, Tele, 0.05);
g = [1; 10; 100; 200; 400; 1000];
throughput = x.*g/sum(x.*g);

% check
x = x/sum(x)
sum(x(5:6))/sum(x)
sum(throughput(5:6))/sum(throughput)