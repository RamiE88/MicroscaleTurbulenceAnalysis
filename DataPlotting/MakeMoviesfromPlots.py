import cv2
import glob

# Get all PNG files in the directory (sorted)
image_files = sorted(glob.glob("path_to_folder/*.png"))  

# Read the first image to get dimensions
frame = cv2.imread(image_files[0])
h, w, _ = frame.shape

# Define video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
out = cv2.VideoWriter("output_video.mp4", fourcc, 10, (w, h))  # 10 FPS

# Add images to video
for img_file in image_files:
    frame = cv2.imread(img_file)
    out.write(frame)

# Release video writer
out.release()

print("Video saved as output_video.mp4")

