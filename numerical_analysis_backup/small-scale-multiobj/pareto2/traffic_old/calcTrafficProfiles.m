clc;
close all;
clear;

Nele = 0.25;
Tele = 0.85;
% f = -[1, 10, 100, 200, 400, 1000];
f = [-1, zeros(1, 3), -1, -1];
% f = -ones(1, 6);
% f = [1, zeros(1, 5)];
x = trafficProfile(f, Nele, Tele, 0.1);
g = [1; 10; 100; 200; 400; 1000];
throughput = x.*g/sum(x.*g)