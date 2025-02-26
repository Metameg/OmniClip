import json
import os
import subprocess
import random
# from AutoEditor import AutoEditor
from app.tools import utilities

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
    
    print("command: " + ' '.join(ffmpeg_command) )
    subprocess.run(ffmpeg_command)

    return out_path

def _get_random_transition():
    transitions = ['fade', 'wipeleft', 'wiperight','wipeup','wipedown','slideleft','slideright','slideup',
        'slidedown','circlecrop','rectcrop','distance','fadeblack','fadewhite','radial','smoothleft','smoothup','smoothdown',
        'circleopen','circleclose','vertopen','vertclose','horzopen','horzclose','dissolve','pixelize','diagtl','diagtr',
        'diagbl','diagbr','hlslice','hrslice','vuslice','vdslice','hblur','fadegrays','wipetl','wipetr','wipebl','wipebr',
        'squeezeh','squeezev','zoomin','fadefast','fadeslow'
    ]


    return random.choice(transitions)

def get_video_frame_rate(file_path):
    ffprobe_command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate",
        "-of", "json",
        file_path
    ]

    try:
        result = subprocess.run(ffprobe_command, capture_output=True, text=True, check=True)
        json_data = json.loads(result.stdout)
        avg_frame_rate_str = json_data["streams"][0]["avg_frame_rate"]
        numerator, denominator = map(int, avg_frame_rate_str.split('/'))
        frame_rate = numerator / denominator
        print("\n\n\n\n",frame_rate, "\n\n\n\n")
        return frame_rate
    
    except subprocess.CalledProcessError as e:
        print(f"Error running ffprobe: {e}")
        return None



# def get_total_frames(video_path):
#     """Use ffprobe to get the total number of frames in a video."""
#     cmd = [
#         "ffprobe",
#         "-v", "error",
#         "-select_streams", "v:0",
#         "-count_frames",
#         "-show_entries", "stream=nb_frames",
#         "-of", "json",
#         video_path
#     ]
#     result = subprocess.run(cmd, capture_output=True, text=True, check=True)
#     data = json.loads(result.stdout)
#     return int(data['streams'][0]['nb_frames'])



# def fix_video_timestamps(video_path):
#     # Create directories for frames
#     frames_dir = os.path.join(utilities.get_root_path(), 'temp', 'frames')
#     os.makedirs(frames_dir, exist_ok=True)

#     temp_video_path = os.path.join(utilities.get_root_path(), 'temp', "video_tmp.mp4")
#     temp_audio_path = os.path.join(utilities.get_root_path(), 'temp', "temp_audio.aac")
#     final_output_path = os.path.join(utilities.get_root_path(), 'temp', "output_audio.mp4")
#     pts_file_path = os.path.join(utilities.get_root_path(), 'temp', "pts.txt")
    
#     # Step 1: Extract audio and video
#     print("Extracting audio...")
#     subprocess.run([
#         "ffmpeg",
#         "-i", video_path,
#         "-q:a", "0",  # Best audio quality
#         "-map", "a",
#         temp_audio_path
#     ], check=True)

#     print("Extracting video...")
#     subprocess.run([
#         "ffmpeg",
#         "-i", video_path,
#         "-c:v", "copy",
#         "-an",  # No audio
#         temp_video_path
#     ], check=True)

    
    
#     total_frames = get_total_frames(temp_video_path)

#     # Create the pts.txt with corrected timestamps
#     with open(pts_file_path, "w") as pts_file:
#         for i in range(total_frames):
#             pts_file.write(f"{i / 30:.3f}\n")

#     print("Fixing video timestamps...")
#     subprocess.run([
#         "D:\Programs\mp4fpsmod\mp4fpsmod64.exe",
#         temp_video_path,
#         "-t", pts_file_path,
#         "-o", temp_video_path
#     ], check=True)

#     print("Muxing audio and video...")
#     subprocess.run([
#         "ffmpeg",
#         "-i", temp_video_path,
#         "-i", temp_audio_path,
#         "-c:v", "copy",
#         "-c:a", "aac",  # Use AAC codec for audio
#         "-strict", "experimental",  # Allow experimental codecs
#         final_output_path
#     ], check=True)


#     print(f"Processed video saved as: {final_output_path}")

#     return final_output_path



def preprocess(video_clips, size):
    processed_paths = []
    for i, clip in enumerate(video_clips, 1):
        old_fps = get_video_frame_rate(clip)
        if old_fps == 60:
            pts = 'PTS/2'
        elif old_fps == 29.97:
            pts = 'PTS/1.001'
        elif old_fps == 25:
            pts = 'PTS*1.2'
        elif old_fps == 24:
            pts = 'PTS*1.25'
        elif old_fps == 15:
            pts = 'PTS*2'
        elif old_fps == 12:
            pts = 'PTS*2.5'
        else:
            pts = 'PTS-STARTPTS'

        
        outpath = os.path.join(utilities.get_root_path(), 'temp', f'processed{i}.mp4')
        # processed_video = os.path.join(utilities.get_root_path(), 'temp', f'video_processed{i}.mp4')
        # processed_audio = os.path.join(utilities.get_root_path(), 'temp', f'audio_processed{i}.mp3')
        if _has_audio(clip):
            audio_flag = ';[0:a]asetpts=N/SR/TB[a]'
            audio_map = '[a]'
        else:
            audio_flag = ';'
            audio_map = '0:a?'

        ffmpeg_command_video = [
            'ffmpeg',
            '-fflags', '+genpts', 
            '-i', clip,
            '-hide_banner',
            # '-loglevel',
            # 'quiet',
            # '-vf', f'scale={size},setsar=1',
            '-filter_complex', f'[0:v]fps=30,setpts=N/FRAME_RATE/TB,scale={size},setsar=1[v]{audio_flag}',
            '-map', '[v]',
            '-map', audio_map,
            '-y',
            # '-r', '30',
            '-c:v', 'libx264',
            '-c:a', 'aac',
            '-async', '1',
            '-strict', 'experimental',
            outpath
        ]
        # ffmpeg_command_video = [
        #     'ffmpeg',
        # [0:a]aresample=async=1[a]
        #     '-i', clip,
        #     '-vf', f'[0:v]scale={size},setsar=1[v0];',
        #     '-r', '30',
        #     '-y',
        #     '-c:v', 'libx264',
        #     '-c:a', 'aac',
        #     '-strict', 'experimental',
        #     processed_video
        # ]
        # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command_video))
        subprocess.run(ffmpeg_command_video)

        # ffmpeg_command_audio = [
        #     'ffmpeg',
        #     '-i', clip,
        #     '-vn',
        #     '-ar', '44100',
        #     '-ac', '2',
        #     '-ab', '192k',
        #     '-y',
        #     processed_audio
        # ]
        # subprocess.run(ffmpeg_command_audio)

        # ffmpeg_command_combined = [
        #     'ffmpeg',
        #     '-i', processed_video,
        #     '-i', processed_audio,
        #     '-map', '0:v',
        #     '-map', '1:a',
        #     '-y',
        #     '-c:v', 'copy',
        #     '-c:a', 'copy',
            
        #     resize_out
        # ]

        # ffmpeg_command = [
        #     'ffmpeg',
        #     '-i', clip,
        #     '-filter_complex', f'[0:v]fps=30,scale={size}[vout];[0:a]atempo=1.0[aout]',
        #     '-map', '[vout]',
        #     '-map', '[aout]',
        #     '-y',
        #     '-c:v', 'libx264',
        #     '-c:a', 'aac',
        #     '-strict', 'experimental',
        #     resize_out
        # ]

        # subprocess.run(ffmpeg_command_combined)
        processed_paths.append(outpath)

    return processed_paths

def get_length(filename):
    result=subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of",
                        "default=nw=1:nk=1", filename],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT)
    
    return float(result.stdout)

# def build_transition_segment(clip1, clip2, fadeout_duration, clip_duration, size, i):
#     outpath = os.path.join(utilities.get_root_path(), 'temp', f'transition_segment{i}.mp4')
#     processed_clips = _resize_clips([clip1, clip2], size)
#     # clip_duration = get_length(clip1)
#     transition = _get_random_transition()
#     OFS = clip_duration - fadeout_duration
#     print("\n\n\n", "clip_duration:", clip_duration, "OFS:", OFS, "\n\n\n")
#     ffmpeg_command = [
#             'ffmpeg',
#             # '-hide_banner',
#             # '-loglevel',
#             # 'quiet',
#             '-i', processed_clips[0],
#             '-i', processed_clips[1],
#             '-filter_complex',
#             f'[0]settb=AVTB,fps=30[v0];[1]settb=AVTB,fps=30[v1]; [0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0]; [1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1]; [v0][v1]xfade=transition={transition}:duration={fadeout_duration}:offset={clip_duration - fadeout_duration},format=yuv420p[vout]; [a0][a1]acrossfade=d={fadeout_duration}[aout]',
#             '-map', "[vout]",
#             '-map', "[aout]",
#             # '-t', f'{clip_duration}',
#             '-y',
#             '-c:v', 'libx264',
#             '-c:a', 'aac',
#             '-strict', 'experimental',
#             outpath
#         ]
#     subprocess.run(ffmpeg_command)

#     return outpath


def concat_videos(video_clips, outpath):
    outpath = os.path.join(utilities.get_root_path(), 'temp',  'transitions_video.mp4' )
    inputs = ''
    for video in video_clips:
        inputs += f'-i {video} ' 
    filter_complex = '"' + f"{''.join([f'[{i}:v:0][{i}:a:0]' for i in range(len(video_clips))])}concat=n={len(video_clips)}:v=1:a=1[vout][aout]" + '"'
    # ffmpeg_command = [
    #     'ffmpeg',
    #     inputs,  
    #     '-filter_complex', filter_complex,
    #     '-map', '[vout]',
    #     '-map', '[aout]',
    #     '-c:v', 'libx264',
    #     '-c:a', 'aac',
    #     outpath
    # ]
    command = 'ffmpeg ' + inputs + ' -filter_complex ' + '"' + filter_complex + '"' + " -map [vout] -map [aout] -c:v libx264 -c:a aac -y " + outpath
    print("\n\n\n", command, "\n\n\n")
    os.system(command)
    # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    # print("\n\n\n", ffmpeg_command_str, "\n\n\n")

    # Run the FFmpeg command
    # subprocess.run(ffmpeg_command)

    return outpath

def build_transitions(video_clips, target_duration, fadeout_duration, size):
    outpath = os.path.join(utilities.get_root_path(), 'temp',  'transitions_video.mp4' )
    # Resize clips 
    resized_clips = preprocess(video_clips, size)

    # If any clip has no audio, add silent audio component to it
    for i, clip in enumerate(resized_clips):
        if not _has_audio(clip):
            print("\n\n\n\n", clip, "is being silenced...")
            resized_clips[i] = _insert_silent(clip)

    # FLV=''
    # FLA=''
    # OFS=0
   
    # PDV=''
    # PDA=''
    # FLV = ''
    # FLA = ''
    file = resized_clips[0]
    resized_clips_length = len(resized_clips)
    transition = _get_random_transition()
    inputs = f'-i {file} '
    XFD=fadeout_duration
    print(file)
    DUR=get_length(file)
    OFS=DUR-XFD
    FCT=1
        
    PDV=f"[{FCT}v]"
    if resized_clips_length <= 2:
        PDV=",format=yuv420p" + f"[{FCT}v]" 
    FLV=f"[0:v][1:v]xfade=transition={transition}:duration={XFD}:offset={OFS}{PDV}"
    PDA=f"[0a]"
    # FLA=f"[0:a]afade=t=out:st={DUR-XFD}:d={XFD}[fadeout0];"
    FLA=f"[0:a]apad,atrim=0:{DUR}{PDA};"
    PDC=f"[01a]"
    FLC=f"[0a][1a]acrossfade=d={XFD}{PDC}"
    # FLC="[fadeout0]"

    if len(resized_clips) == 1:
        command = f'ffmpeg -i "{resized_clips[0]}" -t {target_duration} -c:v libx264 -c:a aac -map_metadata -1 {outpath} -y -hide_banner'
        os.system(command)
    else:
        for i in range(1, len(resized_clips)-1):
        # for i, file in enumerate(resized_clips):
            file = resized_clips[i]
            transition = _get_random_transition()
            DUR = get_length(file)
            OFS = OFS + DUR - XFD
            print("\n\n", OFS ,"XFD:", XFD, "file-dur:", DUR)
            
            # Build string for ffmpeg inputs
            inputs += f'-i {file} '
            
            FCT += 1
            FLV += f";{PDV}[{FCT}:v]xfade=transition={transition}:duration={XFD}:offset={OFS}"
            if i < len(resized_clips) - 2:
                PDV = f"[{FCT}v]"
            else:
                PDV = f",format=yuv420p[{FCT}v]"
            FLV += f"{PDV}"

            PDA = f"[{i}a]"
            # FLA += f"[{i}:a]afade=t=out:st={DUR-XFD}:d={XFD}[fadeout{i}];"
            FLA += f"[{i}:a]apad,atrim=0:{DUR}{PDA};"
            # FLC+=f'[fadeout{i}]'

            FLC += f";{PDC}[{FCT}a]acrossfade=d={XFD}"
            
            PDC = f"[0{FCT}a]"
            FLC += f"{PDC}"
            
            # Pre-process strings for filter_complex
            # PDV += f'[{i}:v]settb=AVTB,fps=30[v{i}];'
            # PDA += f'[{i}:a]aformat=sample_rates=44100:channel_layouts=stereo[a{i}];'
  
        intermediate_video = os.path.join(utilities.get_root_path(), 'temp', 'intermediate_video.mp4')
        intermediate_audio = os.path.join(utilities.get_root_path(), 'temp', 'intermediate_audio.m4a')
        

        file = resized_clips[-1]
        resized_clips_length = len(resized_clips)
        inputs += f"-i {file} "
        DUR = get_length(file)
        PDA = f"[{resized_clips_length-1}a];"
        # FLA += FLC + f'concat=n={resized_clips_length-1}:v=0:a=1[aout]'
        FLA += f"[{resized_clips_length-1}:a]atrim=0:{DUR}{PDA}"
        
        PDV =  PDV.replace(",format=yuv420p", "")
        
        

        video_cmd = f"ffmpeg {inputs} -filter_complex \"{FLV}\" -map {PDV} -c:v libx264 -an -y {intermediate_video} "
        print("ffmpeg_video: ", video_cmd)
        subprocess.run(video_cmd, shell=True)
        # audio_cmd = f"ffmpeg {inputs} -filter_complex \"{FLA}\" -map [aout] -c:a aac -q:a 4 -y {intermediate_audio} -hide_banner"
        audio_cmd = f"ffmpeg {inputs} -filter_complex \"{FLA} {FLC}\" -map {PDC} -c:a aac -q:a 4 -y {intermediate_audio} -hide_banner -loglevel quiet"
        print("\n\nffmpeg_audio: ", audio_cmd)
        subprocess.run(audio_cmd, shell=True)
        comb_cmd = f"ffmpeg -y -i {intermediate_video} -i {intermediate_audio} -af aresample=async=1000 -c:v copy {outpath} -hide_banner -loglevel quiet"
        # command_combined = 'ffmpeg ' + inputs + ' -filter_complex ' + '"' +  FLV  +  FLA + '"' + f' -map [vout] -map [aout] -t {target_duration} -c:v libx264  -c:a aac  -map_metadata -1 {outpath} -y'
        # command = 'ffmpeg ' + inputs + ' -filter_complex ' + '"' + PDV + FLV  + PDA + FLA + '"' + f' -map [vout] -map [aout] -t {target_duration} -c:v libx264  -c:a aac  -map_metadata -1 {outpath} -y -hide_banner'
        print(comb_cmd)
        os.system(comb_cmd)

    # fixed_outpath = fix_video_timestamps(outpath)

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
        '-hide_banner',
        '-loglevel',
        'quiet',
        '-map', '0:v',
        '-map', '1:a',
        # '-t', f'{duration}',
        '-shortest',
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
    
def add_opacity(img, opacity):
    outpath = os.path.join(utilities.get_root_path(), 'temp', f'watermark_opacity.png')
    ffmpeg_command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel',
        'quiet',
        '-i', img,
        '-filter_complex',
        f'[0:v]format=rgba,colorchannelmixer=aa={opacity}[overlay]',
        '-map', '[overlay]',
        '-y',
        '-strict', 'experimental',
        outpath
    ]

    subprocess.run(ffmpeg_command)
    # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    # print(ffmpeg_command_str)
    return outpath

def add_watermark(img, video, opacity):
    outpath = os.path.join(utilities.get_root_path(), 'temp', f'watermark_video.mp4')
    size = '300:180'
    img_resized = _resize_img(img, size)

    img_opacity = add_opacity(img_resized, opacity)
    ffmpeg_command = [
        'ffmpeg',
        '-hide_banner',
        '-loglevel',
        'quiet',
        '-i', video,
        '-i', img_opacity,
        '-filter_complex',
        '[0:v][1:v]overlay=(W-w)/2:25[bg];[bg][1:v]overlay=(W-w)/2:main_h/2-overlay_h/2[bg];[bg][1:v]overlay=(W-w)/2:main_h-overlay_h-25',
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


def add_text(video, font_name=None, font_size=None, ass_file=None, quote=None):
        text_out = os.path.join(utilities.get_root_path(), 'temp', f'text_video.mp4')
        if ass_file:
            ffmpeg_command = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel',
            'quiet',
            '-i', video,
            '-vf',
            f"ass={ass_file}",
            '-c:a', 'copy',
            '-y',
            text_out
        ]
        else:
            ffmpeg_command = [
                'ffmpeg',
                '-hide_banner',
                '-loglevel',
                'quiet',
                '-i', video,
                '-filter_complex',
                f"drawtext=text='{quote}':fontfile={font_name}:fontsize={font_size}:fontcolor=#000000:box=1:boxcolor=black@0.0:boxborderw=5:x=(W-text_w)/2:y=(H-text_h)/2:enable='between(t,0,5)'[text];[0:v][text]overlay=0:0",
                '-c:v', 'libx264',
                '-c:a', 'aac',
                '-y',
                '-strict', 'experimental',
                text_out
            ]

        
        subprocess.run(ffmpeg_command)
        ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
        print("text ffmpeg comd:" , ffmpeg_command_str)
        return text_out








# if __name__ == '__main__':
#     editor = AutoEditor('output', 'video_uploads', 'audio_uploads', 'watermark_uploads', 0.5, 24, 'freedom', 32, 300, '', 'Callum')
#     video_clips = editor.select_random_files(editor.video_folder, True)
#     for f in video_clips: 
#         print(f)
#     build_transitions(video_clips, editor.target_duration, '576x1024')