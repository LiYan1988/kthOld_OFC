clc;
close all;
clear;

load blk2.mat
createfigure(blk(:,11),[blk(:,10), blk(:, 1:9)])