import os
from . import utilities
import whisper_timestamped as whisperts
from whisper_timestamped.make_subtitles import write_srt

def _characters_after_x(input_string, x):
    index_of_x = input_string.find(x)

    if index_of_x != -1:
        result = input_string[index_of_x + 1:]
        return result
    else:
        return None
    

def _seconds_to_ass_time(seconds):
    '''
    Reformatting hours/minutes/seconds/centiseconds into the 
    appropriate format for an .ass file.
    '''
    
    hours = int(seconds / 3600)
    minutes = int((seconds % 3600) / 60)
    seconds = seconds % 60
    centiseconds = int((seconds - int(seconds)) * 100)
    return f"{hours:02}:{minutes:02}:{int(seconds):02}.{centiseconds:02}"


def _create_ass_file(data, font_style='arial', font_size=16, font_stroke=None, size='576x244'):
    '''
        Writes the data to the .ass file using the fields below. (SOME FIELDS GENERATED via ChatGPT!!!)
    '''
    height = _characters_after_x(size, 'x')
    print(height)
    marginv = int(height) // 2 if height else 0
    print("marginv: ", marginv)

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
                     f"0,0,0,0,100,100,0,0.00,1,2,2,2,10,10,{marginv},1")
    ass_lines.append("")
    ass_lines.append("[Events]")
    ass_lines.append("Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text")

    # for i, word in enumerate(data["words"]):
    for word in data:
        start_time = _seconds_to_ass_time(word["start"])
        end_time = _seconds_to_ass_time(word["end"])
        text = word["text"]
        ass_lines.append(f"Dialogue: 0,{start_time},{end_time},Default,,0000,0000,0000,,{text}")

    ass_file = os.path.join(utilities.get_root_path(), 'temp', 'subtitles.ass')
    print("\n\n\n\n\nass_file:", ass_file, "\n\n\n\n")
    with open(ass_file, "w") as f:
        f.write("\n".join(ass_lines))

    
def transcribe_subtitles(audio):
    print("\n\n\n\n\naudio_file: ", audio, "\n\n\n\n\n")
    audio_to_transcribe = whisperts.load_audio(audio)
    model = whisperts.load_model("tiny", device="cpu")

    result = whisperts.transcribe(model, audio_to_transcribe, language="en")
    words = result['segments'][0]['words']

    _create_ass_file(words)

if __name__ == '__main__':
    
    audio = whisperts.load_audio("python\Callum.mp3")
    model = whisperts.load_model("tiny", device="cpu")

    result = whisperts.transcribe(model, audio, language="en")
    words = result['segments'][0]['words']

    for word in words:
        print(word)
    ass_file = os.path.join(utilities.get_root_path(), 'temp', 'subtitles.ass')
    print("\n\n\n\n\nass_file:", ass_file, "\n\n\n\n")
    with open(ass_file, 'w') as file:
    # Your print statement here
        transcribe_subtitles(audio)

    # import json
    # print(json.dumps(result, indent = 2, ensure_ascii = False))
    # print(result['segments'][0]['words'])