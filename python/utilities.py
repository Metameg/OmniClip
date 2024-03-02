import os

def get_root_path():
    this_directory = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.join(this_directory, '..')

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


def get_substring_after_char(input_string, x):
    index_of_x = input_string.find(x)

    if index_of_x != -1:
        result = input_string[index_of_x + 1:]
        return result
    else:
        return None
    

def seconds_to_ass_time(seconds):
    '''
    Reformatting hours/minutes/seconds/centiseconds into the 
    appropriate format for an .ass file.
    '''
    
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    centiseconds = int((seconds - int(seconds)) * 100)
    
    return f"{hours:02}:{minutes:02}:{int(seconds):02}.{centiseconds:02}"



