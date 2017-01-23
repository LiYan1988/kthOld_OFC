function [utilizationEntropyPerSlot, utilizationEntropyPerCore, ...
        utilizationEntropyPerPod] = ...
        utilizationEntropy(matrixResource, numCores)
z = matrixResource;
numSlots = size(z, 2);
numPods = size(z, 1)/numCores;

xp1 = circshift(z, [0, 1]);
xp1(:, 1) = [];
zx = z;
zx(:, 1) = [];
diffCore = abs(zx-xp1);
utilizationEntropyPerCore = mean(diffCore, 2);

yp1 = circshift(z, [1, 0]);
yp1(1, :) = [];
zy = z;
zy(1, :) = [];
diffSlot = abs(zy-yp1);
utilizationEntropyPerSlot = mean(diffSlot, 1);

utilizationEntropyPerPod = zeros(numPods, 1);
for i=1:numPods
    sliceCore = (1+(i-1)*numCores):i*numCores;
    tmpCore = diffCore(sliceCore, :);
    sliceSlot = (1+(i-1)*numCores):(i*numCores-1);
    tmpSlot = diffSlot(sliceSlot, :);
    utilizationEntropyPerPod(i) = (sum(tmpCore(:))+sum(tmpSlot(:)))...
        /((numSlots-1)*numCores+(numCores-1)*numSlots);
end