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


# Writes the data to the .ass file using the fields below. (SOME FIELDS GENERATED via ChatGPT!!!)
def create_ass_file(data, font_style='arial', font_size=16, size='576x524'):
    height = get_substring_after_char(size, 'x')

    marginv = height // 2 if height else 0

    ass_lines = []
    ass_lines.append("[Script Info]")
    ass_lines.append("WrapStyle: 0")
    ass_lines.append("ScaledBorderAndShadow: yes")
    ass_lines.append("YCbCr Matrix: None")
    ass_lines.append("")
    ass_lines.append("[V4+ Styles]")
    ass_lines.append("Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold," 
                     "Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,"
                     "MarginL,MarginR,MarginV,Encoding")
    ass_lines.append(f"Style: Default,{font_style},{font_size},&HFFFFFF,&H000000,&H000000,&H000000,"
                     "0,0,0,0,100,100,0,0.00,1,2,2,2,10,10,{marginv},1")
    ass_lines.append("")
    ass_lines.append("[Events]")
    ass_lines.append("Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text")

    # for i, word in enumerate(data["words"]):
    for word in data["words"]:
        start_time = seconds_to_ass_time(word["start"])
        end_time = seconds_to_ass_time(word["end"])
        text = word["text"]
        ass_lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0000,0000,0000,,{text}")

    ass_file = os.path.join(get_root_path(), 'temp', 'subtitles.ass')
    with open(ass_file, "w") as f:
        f.write("\n".join(ass_lines))


