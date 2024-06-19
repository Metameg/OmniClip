from flask import render_template
import os
from app.tools.utilities import truncate
import re
import mimetypes
import string
import secrets

def classify_file_type(file_path):
    # Create a magic.Magic instance
    mime_type = mimetypes.MimeTypes().guess_type(file_path)[0]
    if mime_type is None:
        return 'unknown'
    
    # Check if the MIME type contains 'audio'
    if 'audio' in mime_type:
        return 'audio'
    # Check if the MIME type contains 'video'
    elif 'video' in mime_type:
        return 'video'
    # Check if the MIME type contains 'image'
    elif 'image' in mime_type:
        return 'img'
   

def get_num_copies(filename, files):
    # Initialize a counter for files containing the substring
    count = 0
    basename = os.path.splitext(filename)[0]
    # Iterate over all files in the directory
    for path in files:
        # Check if the filename contains the substring
        pattern = rf'^{re.escape(basename)}(\(\d+\))*\..*'
        # # Use re.sub to replace the matched substring with an empty string
        # base = re.sub(pattern, '', path)
        # print("base:", base)
        if  re.match(pattern, path):
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
        directory= os.path.dirname(path)
        filename = os.path.basename(path)
        tag_type = classify_file_type(path)
        
        if tag_type == 'video':
            video_content = render_template(template, directory=directory, mediapath=filename, filename_trunc=truncate(filename, 18), tag_type=tag_type)
            html_data[1]["videos"] += video_content

        elif tag_type == 'audio':
            audio_content = render_template(template, directory=directory, mediapath=filename, filename_trunc=truncate(filename, 18), tag_type=tag_type)
            html_data[2]["audios"] += audio_content

        elif tag_type == 'img':
            image_content = render_template(template, directory=directory, mediapath=filename, filename_trunc=truncate(filename, 18), tag_type=tag_type)
            html_data[3]["images"] += image_content
            
        
        # Add file to the all media html data
        aggregate_content = render_template(template, directory=directory, mediapath=filename, filename_trunc=truncate(filename, 18), tag_type=tag_type)
        html_data[0]["allMedia"] += aggregate_content

    return html_data

def generate_key(length):
    alphabet = string.ascii_letters + string.digits
    # Generate a random string of length 10
    random_string = ''.join(secrets.choice(alphabet) for i in range(length))

    return random_string
