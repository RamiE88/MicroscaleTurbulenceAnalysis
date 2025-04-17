
FileDir = '/mnt/d/Documents/CFD/CouetteFlowStudies/CouetteFlow0012/postProcessing/Videos/EnergySpectrum_20pc' #CFD - MD equivalent
#FileDir = '/mnt/d/Documents/Brunel/Data/summary_rhouP_data/postProcessing/Videos/EnergySpectrum'#MD Flow
import cv2
import os

def rename_files_with_leading_zeros(folder, digits=4):
    images = [img for img in os.listdir(folder) if img.endswith(".png")]
    images.sort()  # Sort to maintain order

    for index, image in enumerate(images, start=1):
        new_name = "EnergySpectrum"+f"{index:0{digits}d}.png"  # Format with leading zeros
        old_path = os.path.join(folder, image)
        new_path = os.path.join(folder, new_name)
        os.rename(old_path, new_path)

    print(f"Renamed {len(images)} files with leading zeros.")

def images_to_video(image_folder, output_video, fps=4):
    #rename_files_with_leading_zeros(image_folder)  # Ensure filenames are formatted
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    images.sort()  # Sort lexicographically since filenames have leading zeros
    
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


'''

if __name__ == "__main__":
    folder_path = input("Enter the folder path containing PNG images: ")
    output_path = input("Enter the output video filename (e.g., output.mp4): ")
    fps = int(input("Enter FPS (frames per second, default 30): ") or 30)
    
    images_to_video(folder_path, output_path, fps)

'''


images_to_video(FileDir,'CFDSpectrum20pc.mp4')


