function [x_ave, x_std, x_ci] = get_stat(x, alpha)
% Calculate the average, standard deviation, and (1-alpha) confidence
% interval of vector x.

x_ave = mean(x);
x_std = std(x);
x_n = length(x);
t = tinv(1-alpha, x_n);
conf_int = t*x_std/sqrt(x_n-1);
x_ci = [-conf_int, conf_int];