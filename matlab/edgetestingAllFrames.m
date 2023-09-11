%create video reader object
% obj = VideoReader('E.mp4'); % opens the video feed

%```````````````(not recommend to read all the frames at the beginning)
% frames = read(obj); %reads in data  try use readFrame 
% frames = im2uint8(frames); %converts to a smaller memory unit
% centroids = zeros(2,1,1,size(frames,4)); %x is first
% outputFrames = zeros(size(frames,1),size(frames,2),size(frames,3),size(frames,4)); % sets up 4D matrix
%````````````````````````````````````````````````````
OriginalLocation = [a1(16),a2(16)];   %give original location of the particle for tracking
% OriginalSpeed = [a1(1),a2(1)];   %give original speed location

%get number of frames
w=obj.NumberOfFrames;

%% loop through all frames
for i=1:w
    
    frames = read(obj,i); %reads i-th data  try use    readFrame
    frames = im2uint8(frames); %converts to a smaller memory unit
    x = frames(:,:,:);
    y2 = im2bw(x,imbwvalue);    %set graythresh mannually
    im2 = imcomplement(y2); %invert the image
    % remember to use same parameters across all frames to maintain
    % consistancy
    im2 = imfill(im2, 'holes');
%%
% se = strel('disk',6); %first morphological feature, tune this parameter to see the difference
% im2 = imclose(im2,se); %removes all black spaces that are partially connected to white
% im2 = imopen(y2,se); %removes all white spaces partially connected to black
% se = strel('disk',7); %second morphological feature tune this parameter to see the difference
% im2 = imclose(im2,se); %removes all black spaces that are partially
% im2 = imcomplement(im2);
%figure,imshow(im2);
%     se = strel('disk',7); %first morphological feature
%     im2 = imclose(im2,se); %removes all black spaces that are partially
%     im2 = imopen(y2,se); %removes all white spaces partially connected to black
%     se = strel('disk',6); %second morphological feature
%     im2 = imclose(im2,se); %removes all black spaces that are partially
%     im2 = imcomplement(im2);
    %figure,imshow(im2);   %Show processed image
    outputFrames(:,:,i) = im2; %set output frames
    
    %finds the centroids, define the size of it at the begining will
    %improve speed performance, you can try to do this later
    stat(i).data = regionprops(im2,'centroid'); 
    t_info = regionprops(im2,'centroid');
    stat2(i).data = cat(1,t_info.Centroid);  % make centroid data into array form
    a1=stat2(i).data(:,1);   %store all the centroid into a1 a2
    a2=stat2(i).data(:,2);
    
    %find all the partical distances to the original point
    distance=sqrt((a1- OriginalLocation(1)).^2+(a2- OriginalLocation(2)).^2);   
    data=[a1,a2,distance];
    data1=sortrows(data,3);              %sort all centroid in increasing order

    
    if data1(1,3,1)<=15 %threshold to determine if closest particle is the same one, this value is pixel value
        location(i,:)=[OriginalLocation(1,1),OriginalLocation(1,2)];
        OriginalLocation=[data1(1,1,1),data1(1,2,1)];      %get new original location for next frame
    %if no location info is qualified, set new location to previous one, 
    %this might cause problem if the particle is lost for long time
    else 
        location(i,:)=[OriginalLocation(1,1),OriginalLocation(1,2)];
    end

end
