%save myfile overAllspeed;
clear variables; close all; clc;
%% load video for processing
clc;
%create video reader object
obj = VideoReader('paa05.avi'); % opens the video feed

%threshold for binary image conversion
imbwvalue=0.25;

%read the first frame from video to detect all particles
frame = read(obj,1); %#ok<VIDREAD> %reads i-th data  
%%
%converts to a smaller memory unit(8 bit image)
frame = im2uint8(frame); 
figure, imshow(frame);
x = rgb2gray(frame);
figure,imshow(x);
y2 = imbinarize(x,imbwvalue);    %set graythresh mannually
figure, imshow(y2);
%%
im2 = imcomplement(y2); %invert the image
im2 = imfill(im2, 'holes');
figure,imshow(im2);   
%%
% se = strel('disk',6); %first morphological feature, tune this parameter to see the difference
% im2 = imclose(im2,se); %removes all black spaces that are partially connected to white
% im2 = imopen(y2,se); %removes all white spaces partially connected to black
% se = strel('disk',7); %second morphological feature tune this parameter to see the difference
% im2 = imclose(im2,se); %removes all black spaces that are partially
% im2 = imcomplement(im2);
figure,imshow(im2);
%% fill the holes inside the particles
im2 = imfill(im2, 'holes');
figure,imshow(im2);
%%
outputFrames(:,:,1) = im2; %set output frames
stat(1).data = regionprops(im2,'centroid'); %finds the centroids

t_info = regionprops(im2,'centroid');
stat2(1).data = cat(1,t_info.Centroid);  % make centroid data into array form

%```````````get partical number
q=~outputFrames;
%     L=bwlabel(im2);
%     figure,imshow(L)
figure,imshow(im2); hold on;
a1=stat2(1).data(:,1); %x location info
a2=stat2(1).data(:,2); %y location info
plot(a1,a2,'r.');hold on;
for r=1:size(stat2(1).data,1)
    %number all particle for next step
    text(a1(r),a2(r),num2str(r),'color','red');hold on;
    %hold off;
end

