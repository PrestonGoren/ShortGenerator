from pydub import AudioSegment
import cv2
import os
import re
import subprocess 

def sort_key(filename):
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else 0

def get_audio_duration_ms(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio)

def process_image_for_video(image_path, target_size=(1024, 1920)):
    # Load the original image
    image = cv2.imread(image_path)
    
    # Resize the image to fill the frame vertically
    aspect_ratio = image.shape[1] / image.shape[0]  # width / height
    new_width = int(target_size[1] * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, target_size[1]))
    
    # Crop the sides to maintain the aspect ratio of 1024x1920
    crop_x = int((resized_image.shape[1] - target_size[0]) / 2)
    cropped_image = resized_image[:, crop_x:crop_x + target_size[0]]
    
    # Create a blurred background
    blurred_background = cv2.GaussianBlur(resized_image, (0, 0), sigmaX=15, sigmaY=15)
    
    # Crop the blurred background to fit the final size
    blurred_background_cropped = blurred_background[:, crop_x:crop_x + target_size[0]]
    
    # Overlay the original image onto the blurred background
    overlay_y = int((target_size[1] - image.shape[0]) / 2)
    blurred_background_cropped[overlay_y:overlay_y + image.shape[0], :] = image
    
    return blurred_background_cropped

# Function to generate a cross-fade transition between two images
def cross_fade_transition(image1, image2, transition_frames):
    for i in range(transition_frames):
        alpha = i / transition_frames
        beta = 1.0 - alpha
        yield cv2.addWeighted(image1, beta, image2, alpha, 0)

def generate_video(output_dir):
    # calculate paths
    temp_video_path = f"{output_dir}/temp_video_no_audio.mp4"
    combined_voiceover_path = f"{output_dir}/combined_voiceover.mp3"
    output_video_path = f"{output_dir}/final_video_with_audio.mp4"
    image_dir = f"{output_dir}/images"
    voiceover_dir = f"{output_dir}/voiceovers"

    # Get sorted list of images and voiceovers
    images = sorted([img for img in os.listdir(image_dir) if img.endswith('.png')], key=sort_key)
    voiceovers = sorted([vo for vo in os.listdir(voiceover_dir) if vo.endswith('.mp3')], key=sort_key)
    #prepend the directory to the filenames
    images = [os.path.join(image_dir, img) for img in images]
    voiceovers = [os.path.join(voiceover_dir, vo) for vo in voiceovers]

    # Video parameters
    video_size = (1024, 1920)  # Width, Height
    fps = 24
    transition_frames = int(fps * 0.5)  # 0.5 second transitions

    out = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, video_size)

    #generate frames for video 
    for i, (img_path, vo_path) in enumerate(zip(images, voiceovers)):
        current_frame = process_image_for_video(img_path, video_size)
        
        # Calculate duration and frame count for the voiceover
        duration_ms = get_audio_duration_ms(vo_path)
        total_frame_count = int((duration_ms / 1000) * fps)
        
        # Determine the number of frames after the transition
        remaining_frames_after_transition = total_frame_count - transition_frames

        # If it's not the first image, add a transition, then display remaining frames
        if i > 0:      
            # Add the cross-fade transition
            for frame in cross_fade_transition(previous_frame, current_frame, transition_frames):
                out.write(frame)
        
        # Write the remaining frames of the current image
        for _ in range(remaining_frames_after_transition):
            out.write(current_frame)
        
        # Update previous_frame for the next iteration
        previous_frame = current_frame
    #add an extra 24 frames of the final image
    for _ in range(24):
        out.write(current_frame)

    out.release()

    # Combine all voiceovers into a single track and export
    combined_voiceover = AudioSegment.silent(duration=0)
    for vo_path in voiceovers:
        voiceover = AudioSegment.from_file(vo_path)
        combined_voiceover += voiceover
    combined_voiceover.export(combined_voiceover_path, format="mp3")

    # Merge video and audio using ffmpeg
    subprocess.run([
        'ffmpeg', '-y', '-i', temp_video_path, '-i', combined_voiceover_path
        , '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_video_path
    ], check=True)

    # Cleanup temporary files
    os.remove(temp_video_path)
    os.remove(combined_voiceover_path)

    print(f"Final video with images and voiceovers saved to {output_video_path}")

