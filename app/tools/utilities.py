import os

def get_root_path():
    this_directory = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(this_directory, '..', '..')

    return root_path

def clean_temp():
    transitions = os.listdir(os.path.join(get_root_path(), 'temp'))
    for transition in transitions:
        os.remove(os.path.join(get_root_path(), 'temp', transition))

def move_file_to_output_dir(file, filename):
    output_path = os.path.join(get_root_path(), 'output', filename)
    os.rename(file, output_path)

def get_output_count():
    files = os.listdir('output')
    num_files = len(files)

    return num_files

def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()


def sanitize_filename(filename):
    # Replace spaces with underscores and remove other special characters
    return ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)

def upload_files(files, export_folder):

    for file in files:
        sanitized_filename = sanitize_filename(file.filename)
       
        
        # Save the file to the 'uploads' directory with the sanitized filename
        file.save(os.path.join(export_folder, sanitized_filename))
        # print(test_jpeg(file.getvalue()))

def generate_videos(editor, numvideos):
    videos = []
    for _ in range(numvideos):
        # thread = threading.Thread(target=render_video, args=(editor,))
        # thread.start()
        # thread.join()
        editor.render()
        videopath = sorted(os.listdir('output'))[-1]
        videos.append(videopath)

    return videos

def is_audio_file(filename):
    audio_extensions = ['.mp3', '.wav', '.ogg', '.flac', '.aac', '.wma']  
    return any(filename.lower().endswith(ext) for ext in audio_extensions)

def is_video_file(filename):
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv']  # Add more extensions as needed
    return any(filename.lower().endswith(ext) for ext in video_extensions)

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp']  # Add more extensions as needed
    return any(filename.lower().endswith(ext) for ext in image_extensions)
    
def truncate(str, x):
    if len(str) >= x + 6:
        return str[:x-6] + '...' + str[x-3:]
    elif len(str) > x and len(str) < x + 6:
        return str[:x-9] + str[x-3:]
    else:
        return str


