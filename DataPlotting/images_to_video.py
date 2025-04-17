import cv2
import os

def images_to_video(image_folder, output_video, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Ensure they are in order
    
    if not images:
        print("No PNG images found in the folder.")
        return
    
    first_image = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = first_image.shape
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    for image in images:
        img_path = os.path.join(image_folder, image)
        frame = cv2.imread(img_path)
        video.write(frame)
    
    video.release()
    print(f"Video saved as {output_video}")

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PNG images: ")
    output_path = input("Enter the output video filename (e.g., output.mp4): ")
    fps = int(input("Enter FPS (frames per second, default 30): ") or 30)
    
    images_to_video(folder_path, output_path, fps)

