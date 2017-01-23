function [cnt] = checkResult(fileName, numPods, numCores, numSlots)

[srcVec,dstVec,specVec,coreSrcVec,coreDstVec,coreCntVec,slotCntVec,tfk_slot] = ...
    importFileCnk(fileName);
tensorResource = zeros(numPods, numCores, numSlots);
cnt = 0;
for i=1:length(srcVec)
    src = int64(srcVec(i)+1); % source POD
    dst = int64(dstVec(i)+1); % destination POD
    spec = int64(specVec(i)+1); % spectrum slot index
    slotCnt = int64(slotCntVec(i)); % number of spectrum slots
    coreSrc = int64(coreSrcVec(i)+1); % source core index
    coreDst = int64(coreDstVec(i)+1); % destination core index
    coreCnt = int64(coreCntVec(i)); % number of cores
    tmpSrc = tensorResource(src, coreSrc:(coreSrc+coreCnt-1), ...
        spec:(spec+slotCnt-1));
    tmpDst = tensorResource(dst, coreDst:(coreDst+coreCnt-1), ...
        spec:(spec+slotCnt-1));
    if sum(tmpSrc(:))==0 && sum(tmpDst(:))==0
        tensorResource(src, coreSrc:(coreSrc+coreCnt-1), ...
            spec:(spec+slotCnt-1)) = 1;
        tensorResource(dst, coreDst:(coreDst+coreCnt-1), ...
            spec:(spec+slotCnt-1)) = 1;
    else
        cnt = cnt+1;
    end
end