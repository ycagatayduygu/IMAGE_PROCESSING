import cv2
import os
from scipy.io import loadmat, savemat

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
video_path = r"F:\cagatay_folders\tweezer\RA-L Second attempt data\October 12 2023 15-22-54.mp4"
cap = cv2.VideoCapture(video_path)

# Get total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Ask user for the frame range to cut
start_frame, end_frame = ask_for_frame_range(total_frames)

# Extract additional text from the file name
file_name_without_ext = os.path.splitext(os.path.basename(video_path))[0]

# Set video writer with the same codecs and fps as the original
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Name the output file based on the frame numbers and additional text
output_filename = f"cut_{start_frame}_to_{end_frame}_{file_name_without_ext}.mp4"
output_directory = os.path.dirname(video_path)
output_path = os.path.join(output_directory, output_filename)
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Read and write the specified frame range
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
for frame_number in range(start_frame, end_frame):
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)

# Release video writer and capture objects
cap.release()
out.release()
print(f"Cut video saved as {output_filename}")

# Read the .mat files and extract the relevant data
mat_files = ['ControlInput', 'CaFinal']  # Add your .mat filenames here
for mat_file in mat_files:
    # Construct full path to the .mat file
    mat_path = os.path.join(output_directory, file_name_without_ext + '_' + mat_file )  
    # Load the .mat file
    mat_data = loadmat(mat_path)
    # Assuming the variable inside the .mat file is named the same as the .mat file without the extension
    var_name = os.path.splitext(mat_file)[0]
    # Extract the relevant data using the specified frame range
    # Adjust the indexing if the MATLAB data is 1-indexed
    relevant_data = mat_data[var_name][start_frame+1:end_frame+1, :]
    
    # If the file is 'ControlInput', modify the first two columns
    if mat_file == 'ControlInput':
        # Subtract 255 from the first two columns
        relevant_data[:, :2] -= 256
    
    
    # Create a new .mat file with the relevant data
    new_mat_filename = f"{var_name}_{start_frame}_to_{end_frame}_{file_name_without_ext}.mat"
    new_mat_path = os.path.join(output_directory, new_mat_filename)
    savemat(new_mat_path, {var_name: relevant_data})

    print(f"Relevant data from {mat_file} saved as {new_mat_filename}")
