import cv2
import os
# Function to ask the user for the range of frames
def ask_for_frame_range(total_frames):
    while True:
        start_frame = int(input(f"Enter the start frame number (between 0 and {total_frames-1}): "))
        end_frame = int(input(f"Enter the end frame number (between {start_frame} and {total_frames-1}): "))
        if 0 <= start_frame < end_frame <= total_frames:
            return start_frame, end_frame
        else:
            print(f"Invalid frame numbers. Please try again.")

# Read video file
video_path = r"F:\cagatay_folders\tweezer\RA-L Second attempt data\October 12 2023 15-22-54.mp4"  # Replace with your video path
cap = cv2.VideoCapture(video_path)

# Get total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Ask user for the frame range to cut
start_frame, end_frame = ask_for_frame_range(total_frames)


file_name = os.path.basename(video_path)
additional_text = file_name.split('.')[0]  # This gives you 'October 12 2023 15-05-04'


# Set video writer with the same codecs and fps as the original
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You may change the codec if needed

# Name the output file based on the frame numbers and additional text
output_filename = f"cut_{start_frame}_to_{end_frame}_{additional_text}.mp4"
output_directory = r"F:\cagatay_folders\tweezer\RA-L Second attempt data"  # Replace with your desired path
output_path = output_directory + '\\' + output_filename

#output_path = video_path.rsplit('/', 1)[0] + '/' + output_filename
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Read and write the specified frame range
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
for frame_number in range(start_frame, end_frame):
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

# Release everything
cap.release()
out.release()
print(f"Cut video saved as {output_filename}")
