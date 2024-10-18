from moviepy.editor import VideoFileClip, concatenate_videoclips
import os



def read_video_paths_from_file(filepath):
    video_paths = []
    with open(filepath, 'r') as f:
        for line in f:
            # Each line in the file is formatted as 'file <path>'
            if line.startswith("file"):
                video_path = line.split(' ', 1)[1].strip()  # Extract the path after 'file'
                video_paths.append(video_path)
    return video_paths

def concatenate_videos(direcs, output_file):
    # Load all video clips into a list
    video_clips = []
    
    for video_path in direcs:
        if os.path.exists(video_path):
            video_clips.append(VideoFileClip(video_path))
        else:
            print(f"File {video_path} does not exist and will be skipped.")

    # Concatenate all the video clips
    if video_clips:
        final_clip = concatenate_videoclips(video_clips, method="compose")

        # Write the final concatenated video to an output file
        #final_clip.write_videofile(output_file, codec="libx264", fps=24)
        final_clip.write_videofile(output_file, codec="h264_nvenc", fps=24)
    
        print(f"Concatenation complete. Output saved as {output_file}")
    else:
        print("No valid videos to concatenate.")


text_file_path = 'C:\\Automate\\RedditBot\\Out\\directories.txt'
    
# Read video paths from the text file
video_paths = read_video_paths_from_file(text_file_path)
    
# Output file where concatenated video will be saved
output_video_file = 'C:\\Automate\\RedditBot\\Out\\final_output.mp4'
    
# Concatenate the videos
concatenate_videos(video_paths, output_video_file)
