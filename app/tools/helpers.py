from flask import render_template
import os
from app.tools.utilities import truncate, decode_path
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
    
def classify_custom_upload_files(selected_media):
    video_uploads = []
    audio_uploads = []
    watermark_uploads = []

    for path in selected_media:
        path = decode_path(path)
        
        if classify_file_type(path) == 'video':
            video_uploads.append(path)
        elif classify_file_type(path) == 'audio':
            audio_uploads.append(path)
        elif classify_file_type(path) == 'img':
            watermark_uploads.append(path)

    if len(video_uploads) == 0:
        video_uploads = None
    if len(audio_uploads) == 0:
        audio_uploads = None
    if len(watermark_uploads) == 0:
        watermark_uploads = None

    return {"video_uploads": video_uploads,
            "audio_uploads": audio_uploads,
            "watermark_uploads": watermark_uploads}
            
   

def get_num_copies(filename, files):
    # Initialize a counter for files containing the substring
    numbers = []
    basename = os.path.splitext(filename)[0]
    # Iterate over all files in the directory
    for path in files:
        # Check if the filename contains the substring
        pattern = rf'^{re.escape(basename)}\((\d+)\)\..*'

        match = re.match(pattern, path)
        if  match:
            num = int(match.group(1))
            numbers.append(num)

    return max(numbers) + 1 if numbers else 0

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

def _get_file_size(file):
    file.seek(0, 2)  # Seek to the end of the file
    file_size = file.tell()
    file.seek(0)  # Seek to beggining so file can be saved

    return file_size

def check_storage(file, media_dir, media_files):
    MAX_FILE_SIZE_MB = 20
    MAX_DIRECTORY_SIZE_MB = 100
    MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024
    MAX_DIRECTORY_SIZE = MAX_DIRECTORY_SIZE_MB * 1024 * 1024
    response = {
        "status": "ok",
        "message": ""
    }

    file_size = _get_file_size(file)

    if file_size > MAX_FILE_SIZE:
        response = {
            "status": "error",
            "message": f"File {file.filename} exceeds the size limit of 20 MB."
        }

        return response
    
    directory_size = 0
    for filename in media_files:
        file_path = os.path.join(media_dir, filename)

        with open(file_path, 'rb') as file:
            f_size = _get_file_size(file)
        directory_size += f_size

    if directory_size + file_size > MAX_DIRECTORY_SIZE:
        response = {
            "status": "error",
            "message": f"Insufficient Storage. Storage capacity greater than 100MB."
        }
    
    return response
    

def get_num_user_renders(path):
    
    return len(os.listdir(path))
