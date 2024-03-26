from flask import render_template
import os
from app.tools import utilities
import re

def is_audio_file(filename):
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma']  
    return any(filename.lower().endswith(ext) for ext in audio_extensions)

def is_video_file(filename):
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']  # Add more extensions as needed
    return any(filename.lower().endswith(ext) for ext in video_extensions)

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']  # Add more extensions as needed
    return any(filename.lower().endswith(ext) for ext in image_extensions)

def get_num_copies(filename, files):
    # Initialize a counter for files containing the substring
    count = 0
    basename = os.path.splitext(filename)[0]
    # Iterate over all files in the directory
    for path in files:
        # Check if the filename contains the substring
        print(f"is {filename} in {path}??")
        pattern = rf'^{re.escape(basename)}(\(\d+\))*\..*'
        print("pattern: ", pattern)
        # # Use re.sub to replace the matched substring with an empty string
        # base = re.sub(pattern, '', path)
        # print("base:", base)
        if  re.match(pattern, path):
            print("match")
            count += 1

    return count

def build_media_html(file_paths):
    tag_type = ''
    template = "partials/uploader/all-media.html"
    html_data = [
            {"allMedia": "" },
            {"videos": ""},
            {"audios": ""},
            {"images": ""}
    ]

    video_content = ""
    audio_content = ""
    image_content = ""

    for path in file_paths:
        directory_path = os.path.dirname(path)
        filename = os.path.basename(path)
        print(directory_path, ":  ", filename)
        

        if is_video_file(filename):
            upload_dir =  os.path.join(utilities.get_root_path(), 'video_uploads')
            tag_type = 'video'
            video_content = render_template(template, upload_dirs=[directory_path], mediapaths=[filename], tag_type=tag_type)
            html_data[1]["videos"] += video_content

        elif is_audio_file(filename):
            upload_dir = os.path.join(utilities.get_root_path(), 'audio_uploads')
            tag_type = 'audio'
            audio_content = render_template(template, upload_dirs=[directory_path], mediapaths=[filename], tag_type=tag_type)
            html_data[2]["audios"] += audio_content

        elif is_image_file(filename):
            upload_dir =  os.path.join(utilities.get_root_path(), 'watermark_uploads')
            tag_type = 'img'
            image_content = render_template(template, upload_dirs=[directory_path], mediapaths=[filename], tag_type=tag_type)
            html_data[3]["images"] += image_content
            
        else:
            return "Error! Only upload media files."
        
        
        # Add file to the all media html data
        aggregate_content = render_template(template, upload_dirs=[directory_path], mediapaths=[filename], tag_type=tag_type)
        html_data[0]["allMedia"] += aggregate_content

    return html_data