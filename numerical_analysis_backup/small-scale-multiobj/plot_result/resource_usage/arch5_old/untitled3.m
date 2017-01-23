clc;
close all;
clear;

[srcVec,dstVec,specVec,slotCntVec,tfkSlotVec] = ...
    importFileCnk('milp_cnk_0.00e+00.csv');

numPods = 100;
numCores = 3;
numSlots = 80;
tensorResource = zeros(numPods, numCores, numSlots);
matrixResource = zeros(numPods*numCores, numSlots);
cnt=0;
lastwarn('')
for i=1:length(srcVec)
    src = int64(srcVec(i)+1);
    dst = int64(dstVec(i)+1);
    spec = int64(specVec(i)+1);
    slotCnt = int64(slotCntVec(i));
    tfkSlot = int64(tfkSlotVec(i));
    tmp = tensorResource(src, :, spec:(spec+slotCnt-1));
    if sum(tmp)==0
        tensorResource(src, :, spec:(spec+slotCnt-1)) = 1;
        tensorResource(dst, :, spec:(spec+slotCnt-1)) = 1;
    else
        cnt = cnt+1;
    end
    try 
        error(lastwarn)
    catch
        lastwarn
    end
end

for i=1:numPods
    matrixResource(((i-1)*numCores+1):(i*numCores), :) = ...
        squeeze(tensorResource(i, :, :));
end