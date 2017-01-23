clear;
close all;
clc;

filename = 'result_ilps_pod200.csv';
[arch1_ub,arch1_lb,arch2_ub,arch2_lb,arch4_ub,arch4_lb,arch5_ub,arch5_lb,total_cnk] = importfile(filename);
arch1_blkr = 1-arch1_lb./total_cnk;
arch2_blkr = 1-arch2_lb./total_cnk;
arch4_blkr = 1-arch4_lb./total_cnk;
arch5_blkr = 1-arch5_lb./total_cnk;
alpha = 0.05;
[arch1_ave,arch1_std,arch1_ci] = get_stat(arch1_lb, alpha);
[arch2_ave,arch2_std,arch2_ci] = get_stat(arch2_lb, alpha);
[arch4_ave,arch4_std,arch4_ci] = get_stat(arch4_lb, alpha);
[arch5_ave,arch5_std,arch5_ci] = get_stat(arch5_lb, alpha);
pod200_ave = [arch1_ave, arch2_ave, arch4_ave, arch5_ave];
pod200_errl = [arch1_ci(1), arch2_ci(1), arch4_ci(1), arch5_ci(1)];
pod200_erru = [arch1_ci(2), arch2_ci(2), arch4_ci(2), arch5_ci(2)];
figure; hold on;
bar(pod200_ave);
errorbar(1:4,pod200_ave,pod200_errl,pod200_erru,'.');
pod200 = [pod200_ave; pod200_errl; pod200_erru];
csvwrite('pod200.csv', pod200)