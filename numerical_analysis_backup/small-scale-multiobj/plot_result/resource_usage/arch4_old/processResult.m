function [matrixResource, rupcPerCore, rupcPerPod, obj, ...
    uePerSlot, uePerCore, uePerPod] = ...
    processResult(beta, method, numPods, numCores, numSlots)
% beta: value of beta
% method: 'heuristic' or 'milp'

%% Matrix of resource usage
fileNameCnk = strcat(method, '_cnk_', sprintf('%.2e',beta), '.csv');
[srcVec,dstVec,specVec,slotCntVec,tfkSlotVec] = importFileCnk(fileNameCnk);
trafficMatrix = importFileTrafficMatrix('traffic_matrix.csv');

tensorResource = zeros(numPods, numCores, numSlots);
matrixResource = zeros(numPods*numCores, numSlots);
cnt = 0;
obj = 0;
for i=1:length(srcVec)
    src = int64(srcVec(i)+1);
    dst = int64(dstVec(i)+1);
    spec = int64(specVec(i)+1);
    slotCnt = int64(slotCntVec(i));
    tmp = tensorResource(src, :, spec:(spec+slotCnt-1));
    if sum(tmp)==0
        tensorResource(src, :, spec:(spec+slotCnt-1)) = 1;
        tensorResource(dst, :, spec:(spec+slotCnt-1)) = 1;
        obj = obj+1+beta*trafficMatrix(src, dst);
    else
        cnt = cnt+1;
    end
end

for i=1:numPods
    matrixResource(((i-1)*numCores+1):(i*numCores), :) = ...
        squeeze(tensorResource(i, :, :));
end

rupc = sum(matrixResource, 2)/numSlots;
rupcPerCore = mean(rupc);
rupcPerPod = mean(sum(sum(tensorResource, 2), 3)/(numSlots*numCores));

[uePerSlot, uePerCore, uePerPod] = ...
    utilizationEntropy(matrixResource, numCores);
uePerSlot = mean(uePerSlot);
uePerCore = mean(uePerCore);
uePerPod = mean(uePerPod);