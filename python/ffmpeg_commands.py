import os
import subprocess
import random
# from AutoEditor import AutoEditor
from . import utilities

def _resize_img(img, size):
        extension = utilities.get_file_extension(img)
        out_path = os.path.join(utilities.get_root_path(), 'temp', f'img_resize{extension}')

        ffmpeg_command = [
                'ffmpeg',
                '-hide_banner',
                '-loglevel',
                'quiet',
                '-pix_fmt', 'yuv420p',
                '-color_range', '2',
                '-i', img,
                '-vf',
                f'scale={size}',
                '-y',
                out_path
            ]
        
        subprocess.run(ffmpeg_command)

        return out_path

def _resize_clips(clips, size):
    resize_paths = []

    for i, clip in enumerate(clips, 1):
        resize_out = os.path.join(utilities.get_root_path(), 'temp', f'resize{i}.mp4')
        ffmpeg_command = [
                        'ffmpeg',
                        '-hide_banner',
                        '-loglevel',
                        'quiet',
                        '-i', clip,
                        '-vf',
                        f'[0:v]scale={size},setsar=1[v0];',
                        '-y',
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-strict', 'experimental',
                        resize_out
                    ]
        subprocess.run(ffmpeg_command)
        resize_paths.append(resize_out)

    return resize_paths
    
def _get_length(filename):
    result=subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=nw=1:nk=1", filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    
    return float(result.stdout)

def _concat_audios(audios):
    outpath = os.path.join(utilities.get_root_path(), 'temp', f'audios_concat.mp3')

    inputs = ''
    filter_complex = ''
    for i, audio in enumerate(audios):
        if i < len(audios) - 1:
            inputs += f'-i "{audio}" '
        else:
            inputs += f'-i "{audio}"'
        filter_complex += f'[{i}:a]'
    filter_complex += f'concat=n={len(audios)}:v=0:a=1[out]'
    
    command = 'ffmpeg ' + inputs + ' -filter_complex ' + '"' + filter_complex + '"' + " -map [out] -c:a mp3 -y " + outpath
   
    # print("\n\n\n\nCONCAT:",command,"\n\n\n\n\n")

    os.system(command)

    return outpath

def _has_audio(file_path):
    command = ['ffmpeg', '-i', file_path]
    result = subprocess.run(command, capture_output=subprocess.PIPE, text=subprocess.PIPE)
    output = result.stderr
    

    # Check if the output contains information about an audio stream
    return 'Audio' in output

def _insert_silent(file_path):
    file_name_with_extension = os.path.basename(file_path)
    file_name, extension = os.path.splitext(file_name_with_extension)
    out_path = os.path.join(utilities.get_root_path(), 'temp', f'{file_name}_silent{extension}')
    silent_path = os.path.join(utilities.get_root_path(), 'static', 'media', 'silence.mp3')

    ffmpeg_command = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel',
            'quiet',
            '-i', file_path,
            '-i', silent_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-y',
            '-strict', 'experimental',
            '-shortest',
            out_path
        ]
    
    subprocess.run(ffmpeg_command)

    return out_path

def _get_random_transition():
    transitions = ['fade', 'wipeleft', 'wiperight','wipeup','wipedown','slideleft','slideright','slideup',
        'slidedown','circlecrop','rectcrop','distance','fadeblack','fadewhite','radial','smoothleft','smoothup','smoothdown',
        'circleopen','circleclose','vertopen','vertclose','horzopen','horzclose','dissolve','pixelize','diagtl','diagtr',
        'diagbl','diagbr','hlslice','hrslice','vuslice','vdslice','hblur','fadegrays','wipetl','wipetr','wipebl','wipebr',
        'squeezeh','squeezev','zoomin','fadefast','fadeslow','hrwind','vuwind','vdwind','coverleft','coverright',
        'coverup','coverdown','revealleft','revealright','revealup','revealdown'
    ]

    return random.choice(transitions)




def build_transitions(video_clips, target_duration, fadeout_duration, size):
    outpath = os.path.join(utilities.get_root_path(), 'temp',  'transitions_video.mp4' )
    # Resize clips 
    resized_clips = _resize_clips(video_clips, size)

    # If any clip has no audio, add silent audio component to it
    for i, clip in enumerate(resized_clips):
        if not _has_audio(clip):
            print("\n\n\n\n", clip, "is being silenced...")
            resized_clips[i] = _insert_silent(clip)

    FLV=''
    FLA=''
    OFS=0
    XFD=fadeout_duration
   
    PDV=''
    PDA=''
    FLV = ''
    FLA = ''
    inputs = ''

    if len(resized_clips) == 1:
        command = f'ffmpeg -i "{resized_clips[0]}" -t {target_duration} -c:v libx264 -cq 18 -c:a aac -q:a 4 -map_metadata -1 {outpath} -y -hide_banner'

    else:
        for i, file in enumerate(resized_clips):
            transition = _get_random_transition()
            OFS=OFS+_get_length(file)-XFD
            
            # Build string for ffmpeg inputs
            inputs += f'-i {resized_clips[i]} '
            
            # Pre-process strings for filter_complex
            PDV += f'[{i}:v]settb=AVTB,fps=30[v{i}];'
            PDA += f'[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[a{i}];'

            # Build xfade string
            if i == 0:
                FLV += f'[v{i}][v{i+1}]xfade=transition={transition}:offset={OFS}:duration={XFD}'
                FLA += f'[a{i}][a{i+1}]acrossfade=d={XFD}'
            elif i < len(resized_clips)-2:
                FLV += f'[v{i-1}{i}][v{i+1}]xfade=transition={transition}:offset={OFS}:duration={XFD}'
                FLA += f'[a{i-1}{i}][a{i+1}]acrossfade=d={XFD}'
            elif i == len(resized_clips)-2:
                FLV += f'[v{i-1}{i}][v{i+1}]xfade=transition={transition}:offset={OFS}:duration={XFD}'
                FLA += f'[a{i-1}{i}][a{i+1}]acrossfade=d={XFD}'

            # Handle clip labels
            if i == len(resized_clips) - 2:
                FLV += ',format=yuv420p[vout];'
                FLA += '[aout];'
            elif i < len(resized_clips)-2:
                FLV += f'[v{i}{i+1}];'
                FLA += f'[a{i}{i+1}];'
  
        command = 'ffmpeg ' + inputs + ' -filter_complex ' + '"' + PDV + FLV + PDA + FLA + '"' + f' -map [vout] -map [aout] -t {target_duration} -c:v libx264 -q:v 18 -c:a aac -q:a 4 -map_metadata -1 {outpath} -y -hide_banner'

    os.system(command)

    return outpath



def add_audio(video, audios, duration):
    outpath = os.path.join(utilities.get_root_path(), 'temp', f'transition_with_audio.mp4')

    # Set relative paths to audio files
    input_files = []
    for file in audios:
        input_files.append(os.path.join(utilities.get_root_path(), file))
    # Concatenate audios to single mp3
    audio = _concat_audios(input_files)
    
    ffmpeg_command = [
        'ffmpeg',
        '-i', video,
        '-i', audio,
        '-map', '0:v',
        '-map', '1:a',
        '-t', f'{duration}',
        '-c:v', 'copy',
        '-c:a', 'mp3',
        '-strict', 'experimental',
        '-y',
        outpath
    ]
    subprocess.run(ffmpeg_command)
    # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    # print("\n\n\n", ffmpeg_command_str, "\n\n\n")
    
    return outpath
    
def add_watermark(img, video):
    outpath = os.path.join(utilities.get_root_path(), 'temp', f'watermark_video.mp4')
    size = '300:180'
    img_resized = _resize_img(img, size)
    ffmpeg_command = [
        'ffmpeg',
        # '-hide_banner',
        # '-loglevel',
        # 'quiet',
        '-i', video,
        '-i', img_resized,
        '-filter_complex',
        f'[1:v]format=rgba,colorchannelmixer=aa=0.5[overlay];[0:v][overlay]overlay=10:10[video]',
        '-map', '[video]',
        '-map', '0:a',
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-y',
        '-strict', 'experimental',
        outpath
    ]

    
    subprocess.run(ffmpeg_command)
    # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    # print(ffmpeg_command_str)
    return outpath
    
def add_voice_over(video, voice):

    outpath = os.path.join(utilities.get_root_path(), 'temp', f'voice_video.mp4')
    
    ffmpeg_command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel',
        'quiet',
        '-i', video,
        '-i', voice,
        '-filter_complex',
        f"[0:a]volume=1.0[a0];[1:a]volume=3.5[a1];[a0][a1]amix=inputs=2[aout]",
        '-map', '0:v',
        '-map', '[aout]',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-y',
        '-strict', 'experimental',
        outpath
    ]

    
    subprocess.run(ffmpeg_command)
    # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    # print(ffmpeg_command_str)
    return outpath


def add_text(video, font_style, font_size, ass_file=None, quote=None):
        text_out = os.path.join(utilities.get_root_path(), 'temp', f'text_video.mp4')
        if ass_file:
            print("\n\n\n\n\nass_file ffmpeg: ", ass_file, "\n\n\n\n\n")
            ffmpeg_command = [
            'ffmpeg',
            # '-hide_banner',
            # '-loglevel',
            # 'quiet',
            '-i', video,
            '-vf',
            f"ass='{ass_file}",
            '-c:a', 'copy',
            '-y',
            text_out
        ]
        else:
            ffmpeg_command = [
                'ffmpeg',
                # '-hide_banner',
                # '-loglevel',
                # 'quiet',
                '-i', video,
                '-filter_complex',
                f"drawtext=text='{quote}':fontfile={font_style}:fontsize={font_size}:fontcolor=#000000:box=1:boxcolor=black@0.0:boxborderw=5:x=(W-text_w)/2:y=(H-text_h)/2:enable='between(t,0,5)'[text];[0:v][text]overlay=0:0",
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-y',
                '-strict', 'experimental',
                text_out
            ]

        
        subprocess.run(ffmpeg_command)
        # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
        # print(ffmpeg_command_str)
        return text_out








# if __name__ == '__main__':
#     editor = AutoEditor('output', 'video_uploads', 'audio_uploads', 'watermark_uploads', 0.5, 24, 'freedom', 32, 300, '', 'Callum')
#     video_clips = editor.select_random_files(editor.video_folder, True)
#     for f in video_clips: 
#         print(f)
#     build_transitions(video_clips, editor.target_duration, '576x1024')