import os
import urllib
import re

def get_root_path():
    this_directory = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(this_directory, '..')

    return root_path

def clean_temp():
    files = os.listdir(os.path.join(get_root_path(), 'temp'))
    for file in files:
        if os.path.isfile(os.path.join(get_root_path(), 'temp', file)):
            os.remove(os.path.join(get_root_path(), 'temp', file))

def clear_directory(directory):
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if the path is a file
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)

def move_file_to_output_dir(username, from_name, to_name):
    output_path = os.path.join(username, to_name)
    os.rename(from_name, output_path)

def get_media_dir(username):
    return os.path.join(get_root_path(), '..', 'userData', username)


def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()

def split_filename(file_path):
    return os.path.splitext(file_path)
    

def sanitize_filename(filename):
    # Replace spaces with underscores and remove other special characters
    return ''.join(c if c.isalnum() or c in ['.', '_', '-'] else '_' for c in filename)

def upload_files(files, export_folder):

    for file in files:
        sanitized_filename = sanitize_filename(file.filename)
       
        # Save the file to the 'uploads' directory with the sanitized filename
        file.save(os.path.join(export_folder, sanitized_filename))
        # print(test_jpeg(file.getvalue()))

def generate_videos(editor, numvideos, out_dir):
    videos = []
    for _ in range(numvideos):
        # thread = threading.Thread(target=render_video, args=(editor,))
        # thread.start()
        # thread.join()
        editor.render()
        videopath = sorted(os.listdir(out_dir))[-1]
        videos.append(videopath)

    return videos

    
def truncate(str, x):
    if len(str) >= x + 6:
        return str[:x-6] + '...' + str[x-3:]
    elif len(str) > x and len(str) < x + 6:
        return str[:x-9] + str[x-3:]
    else:
        return str

def get_file_size(file):
    file.seek(0, 2)  # Move the file pointer to the end of the file
    file_size = file.tell()  # Get the current position of the file pointer (which is the size of the file)

    return file_size

    
def decode_path(path_with_percent):
    print(path_with_percent)
    # Decode the path with percent-encoded characters
    decoded_path = urllib.parse.unquote(path_with_percent)

    # Replace backslashes with forward slashes
    normalized_path = path_with_percent.replace('%5C', '/')
    
    if normalized_path[0] == '/':
        normalized_path = normalized_path[1:]

    return normalized_path

def decode_and_clean_paths(url_paths):
    cleaned_paths = []
    for url_path in url_paths:
        # Decode the URL-encoded path twice to handle double encoding
        decoded_path = urllib.parse.unquote(urllib.parse.unquote(url_path))
        
        # Replace any remaining %2F with a forward slash
        # clean_path = decoded_path.replace('%2F', '/')
        
        cleaned_paths.append(decoded_path)
    
    return cleaned_paths

import os
import re

def convert_ffmpeg_ass_path(path):
    # Normalize the path to resolve '..' properly
    normalized_path = os.path.normpath(path)

    # Replace backslashes `\` with forward slashes `/`
    escaped_path = normalized_path.replace("\\", "/")

    # Escape the colon in the drive letter (e.g., `D:` → `D\:`)
    escaped_path = re.sub(r"^([A-Za-z]):", r"\1\\\:", escaped_path)

    # Add extra `\` before each `/`
    escaped_path = escaped_path.replace("/", "/\\")

    # Prefix with `ass=`
    return escaped_path






