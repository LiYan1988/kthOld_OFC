clear;
clc;
close all;

filename='result_sa_pod150.csv';
[Arch2_bench1,Arch2_bench2,Arch2_sa,Arch4_bench1,Arch4_bench2,Arch4_sa,Arch5_bench1,Arch5_bench2,Arch5_sa] = importfile_sa(filename);
alpha = 0.05;
[arch2_bench1_ave,arch2_bench1_std,arch2_bench1_ci] = get_stat(Arch2_bench1, alpha);
[arch2_bench2_ave,arch2_bench2_std,arch2_bench2_ci] = get_stat(Arch2_bench2, alpha);
[arch2_sa_ave,arch2_sa_std,arch2_sa_ci] = get_stat(Arch2_sa, alpha);
[arch4_bench1_ave,arch4_bench1_std,arch4_bench1_ci] = get_stat(Arch4_bench1, alpha);
[arch4_bench2_ave,arch4_bench2_std,arch4_bench2_ci] = get_stat(Arch4_bench2, alpha);
[arch4_sa_ave,arch4_sa_std,arch4_sa_ci] = get_stat(Arch4_sa, alpha);
[arch5_bench1_ave,arch5_bench1_std,arch5_bench1_ci] = get_stat(Arch5_bench1, alpha);
[arch5_bench2_ave,arch5_bench2_std,arch5_bench2_ci] = get_stat(Arch5_bench2, alpha);
[arch5_sa_ave,arch5_sa_std,arch5_sa_ci] = get_stat(Arch5_sa, alpha);
pod150_ave = [[arch2_bench1_ave,arch4_bench1_ave,arch5_bench1_ave]; [arch2_bench2_ave,arch4_bench2_ave,arch5_bench2_ave]; [arch2_sa_ave,arch4_sa_ave,arch5_sa_ave]];

load 'pod150.csv';
pod150_ave = [pod150_ave; [pod150(1,2:end)]];
a = pod150_ave(3,1);
pod150_ave(3, 1) = pod150_ave(4,1);
pod150_ave(4,1)=a;
figure; hold on;
bar(pod150_ave');
csvwrite('pod150_final.csv',pod150_ave);