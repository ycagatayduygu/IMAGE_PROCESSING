import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read video file
video_path = r"F:\cagatay_folders\planar\data\septemebr 2022\dataselect\video_cut.mp4"
cap = cv2.VideoCapture(video_path)

# Read the first frame
ret, frame = cap.read()

if not ret:
    print("Error reading video frame.")
    exit()

# Convert the frame to grayscale
gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
plt.figure(figsize=(10, 6))

# Display the original frame
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Original Frame")

# Display the grayscale frame
plt.subplot(2, 2, 2)
plt.imshow(gray_frame, cmap='gray')
plt.title("Grayscale")

# Apply thresholding to the grayscale frame
_, binary_frame = cv2.threshold(gray_frame, 50, 255, cv2.THRESH_BINARY)
plt.subplot(2, 2, 3)
plt.imshow(binary_frame, cmap='gray')
plt.title("Binary Thresholding")

# Invert the binary frame and fill holes
inverted_frame = cv2.bitwise_not(binary_frame)
filled_frame = cv2.morphologyEx(inverted_frame, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
filled_frame = cv2.bitwise_not(filled_frame)
plt.subplot(2, 2, 4)
plt.imshow(filled_frame, cmap='gray')
plt.title("Inverted and Holes Filled")


# Find contours in the filled_frame
contours, _ = cv2.findContours(filled_frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
print("Number of contours:", len(contours))

# Define a minimum contour area threshold
min_contour_area = 50  # Adjust this value according to your needs

# Filter out small contours based on area
filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

# Exclude the first contour from filtered_contours
filtered_contours = filtered_contours[1:]

print("Number of filtered contours:", len(filtered_contours))

# Draw centroids and numbers
for i, contour in enumerate(filtered_contours):
    moments = cv2.moments(contour)
    if moments["m00"] != 0:
        centroid_x = int(moments["m10"] / moments["m00"])
        centroid_y = int(moments["m01"] / moments["m00"])
        cv2.circle(frame, (centroid_x, centroid_y), 3, (0, 0, 255), -1)
        cv2.putText(frame, str(i + 1), (centroid_x + 5, centroid_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        print(centroid_x, centroid_y)

# Display the frame with centroids and numbers
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Centroids Numbered")


plt.tight_layout()
plt.show()


# Display the first frame and prompt user to select a contour
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("First Frame: Select Contour to Track")
plt.show()

# Choose the contour index to track based on user input
contour_to_track = int(input("Enter the index of the contour to track: "))

# Create a VideoWriter to save the output video

output_video_path = r"F:\cagatay_folders\planar\data\septemebr 2022\dataselect\centroid_tracking_output3.avi"
#output_video_path = r"F:\cagatay_folders\planar\data\septemebr 2022\dataselect\centroid_tracking_output2.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (frame.shape[1], frame.shape[0]))


# Initialize lists for trajectory points and rainbow colors
trajectory = []
rainbow_colors = plt.cm.rainbow(np.linspace(0, 1, len(filtered_contours)))

# Track the selected contour in subsequent frames
while True:
    ret, frame = cap.read()

    if not ret:
        print("End of video.")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, binary_frame = cv2.threshold(gray_frame, 64, 255, cv2.THRESH_BINARY)
    inverted_frame = cv2.bitwise_not(binary_frame)
    filled_frame = cv2.morphologyEx(inverted_frame, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)))
    filled_frame = cv2.bitwise_not(filled_frame)
    
    contours, _ = cv2.findContours(filled_frame, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]
    filtered_contours = filtered_contours[1:]
    
    found_contour = False
    color_idx = 0  # Initialize index for color cycling
    
    for i, contour in enumerate(filtered_contours):
        if i == contour_to_track - 1:  # Subtract 1 for 0-based index
            moments = cv2.moments(contour)
            if moments["m00"] != 0:
                centroid_x = int(moments["m10"] / moments["m00"])
                centroid_y = int(moments["m01"] / moments["m00"])
                cv2.circle(frame, (centroid_x, centroid_y), 3, (0, 0, 255), -1)
                cv2.putText(frame, str(i + 1), (centroid_x + 5, centroid_y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                #print(centroid_x, centroid_y)
                found_contour = True
                break
    
# ...
    
    if found_contour:
        # Calculate the distance between the current and previous centroid positions
        if len(trajectory) > 0:
            prev_x, prev_y = trajectory[-1]
            distance = np.sqrt((centroid_x - prev_x)*2 + (centroid_y - prev_y)*2)
            
            # If the distance is too large, use the previous position
            if distance > 10:
                centroid_x, centroid_y = prev_x, prev_y
        
        # Append centroid coordinates to the trajectory list
        trajectory.append((centroid_x, centroid_y))
        
        # Draw the trajectory on the frame using rainbow colors
        color_idx = 0  # Initialize index for color cycling
        for j in range(len(trajectory)):
            cv2.circle(frame, trajectory[j], 2, rainbow_colors[color_idx], -1)
            color_idx = (color_idx + 1) % len(rainbow_colors)
        
        cv2.imshow("Centroid Tracked", frame)


    
    out.write(frame)
    #cv2.imshow("Tracked Contour", frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

# # -- coding: utf-8 --
"""
Created on Wed Aug 30 17:13:57 2023

@author: 48369962
"""