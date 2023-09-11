%% Plot Centroids on input frames
close all;
%create centroid movie object
v = VideoWriter('alas_deneme8.mp4','MPEG-4');
%set frame rate number
v.FrameRate = 30;
%open video writer object
open(v);
j=1;
totalFrames = w;
F(w) = struct();
F(1).cdata = zeros(720,720,3);
F(1).colormap = [];
cmap = jet(w);

%set(gcf, 'position', [0 0 1200 500]);
for i=1:totalFrames
    frames1 = read(obj,i); %reads i-th data  try use readFrame
    frames1 = im2uint8(frames1); %converts to a smaller memory unit
    x1 = frames1(:,:,:);
    %subplot(1,2,1),
    imshow(x1,'Border','tight');hold on;
    %plot location history up to current frame
    
    %plot(location(1:i,1),location(1:i,2),cmap(1:i,:),'linewidth',3.5);
    %plot(location(1:i,1), location(1:i,2),'Color' ,cmap(1:i,:),'fill');
    %plot(location(1:i,1),location(1:i,2),30,cmap(1:i,:),'fill')
    %scatter(location(1:i,1),location(1:i,2),30,cmap(1:i,:),'fill')
    plot(location_16(1:i,1),location_16(1:i,2),'-y','linewidth',3.5);
    plot(location_22(1:i,1),location_22(1:i,2),'-g','linewidth',3.5);
    plot(location_26(1:i,1),location_26(1:i,2),'-r','linewidth',3.5);
    plot(location_27(1:i,1),location_27(1:i,2),'-b','linewidth',3.5);
    
    
    
    %% All
%     plot(location1(1:i,1),location1(1:i,2),'-b','linewidth',3.5);
%     
%     plot(location19(1:i,1),location19(1:i,2),'-r','linewidth',3.5);
%     
%     plot(location119(1:i,1),location119(1:i,2),'-g','linewidth',3.5);
%     %plot(location2(1:i,1),location2(1:i,2),'-c','linewidth',3.5);
%     plot(location22(1:i,1),location22(1:i,2),'-', 'Color', [0.4940 0.1840 0.5560],'linewidth',3.5);
% 
%     plot(location27(1:i,1),location27(1:i,2),'-y','linewidth',3.5);
%     plot(location39(1:i,1),location39(1:i,2),'-w','linewidth',3.5);
%     
%     plot(location41(1:i,1),location41(1:i,2),'-', 'Color', [162 20 47]/255,'linewidth',3.5);
%     plot(location45(1:i,1),location45(1:i,2),'-', 'Color', [0.8500 0.3250 0.0980],'linewidth',3.5);
%     plot(location_59(1:i,1),location_59(1:i,2),'-', 'Color', [0.9290 0.6940 0.1250],'linewidth',3.5);
% 
%     plot(location6(1:i,1),location6(1:i,2),'-', 'Color', [0.9290 0.6940 0.1250],'linewidth', 3.5);
% 
%     if i>24
%     plot(location_half1(1:i-24,1),location_half1(1:i-24,2),'-', 'Color', [0.4660 0.6740 0.1880],'linewidth', 3.5);
%     end
%    
%     if i>14
%     plot(location_half2(1:i-14,1),location_half2(1:i-14,2),'-', 'Color', [0 0.4470 0.7410],'linewidth', 3.5);
%     end
    
% 
% 
% 

%%
    hold off;
    %store frames with tracking trajectory in struct F
    F(i)=getframe(gcf);
    
end
%write F to video
writeVideo(v,F);
close(v);
%centroid trajectory
%save('27_2_location.mat', 'location')