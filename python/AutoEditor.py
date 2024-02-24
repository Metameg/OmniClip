import os
from datetime import datetime
import time
import ffmpeg
import random
from . import utils
from . import ffmpeg_commands as fmpgapi
# from proglog import ProgressBarLogger

# class MyBarLogger(ProgressBarLogger):
#     def __init__(self):
#         super().__init__()
#         self.percentage = 0  # Initialize percentage
#         # self.progress_bar = st.progress(0)  # Create progress bar

#     def bars_callback(self, bar, attr, value, old_value=None):
#         # Every time the logger progress is updated, this function is called
#         self.percentage = (value / self.bars[bar]['total']) * 100
#         # self.progress_bar.progress(self.percentage / 100)


class AutoEditor():
    def __init__(self, export_folder, video_folder, audio_folder, overlay_folder, fade_duration, target_duration, font_style, font_size, font_stroke, quote=None, voice=None):
        self.export_folder = export_folder
        self.fade_duration = fade_duration
        self.target_duration = target_duration
        self.video_folder = video_folder
        self.audio_folder = audio_folder
        self.overlay_folder = overlay_folder
        self.font_style = 'font_ttfs/' + font_style + '.ttf'
        self.font_size = font_size
        self.font_stroke = font_stroke
        self.quote = quote
        self.voice = voice
        

    # def _has_audio(self, file_path):
    #     command = ['ffmpeg', '-i', file_path]
    #     result = subprocess.run(command, capture_output=subprocess.PIPE, text=subprocess.PIPE)
    #     output = result.stderr
        

    #     # Check if the output contains information about an audio stream
    #     return 'Audio' in output
    
    # def _insert_silent(self, file_path):
    #     file_name_with_extension = os.path.basename(file_path)
    #     file_name, extension = os.path.splitext(file_name_with_extension)
    #     out_path = os.path.join(utils.get_root_path(), 'temp', f'{file_name}_silent{extension}')
    #     silent_path = os.path.join(utils.get_root_path(), 'static', 'media', 'silence.mp3')

    #     ffmpeg_command = [
    #             'ffmpeg',
    #             '-hide_banner',
    #             '-loglevel',
    #             'quiet',
    #             '-i', file_path,
    #             '-i', silent_path,
    #             '-c:v', 'copy',
    #             '-c:a', 'aac',
    #             '-y',
    #             '-strict', 'experimental',
    #             '-shortest',
    #             out_path
    #         ]
        
    #     subprocess.run(ffmpeg_command)

    #     return out_path
    
    # def _resize_img(self, img, size):
    #     extension = utils.get_file_extension(img)
    #     out_path = os.path.join(utils.get_root_path(), 'temp', f'img_resize{extension}')

    #     ffmpeg_command = [
    #             'ffmpeg',
    #             '-hide_banner',
    #             '-loglevel',
    #             'quiet',
    #             '-pix_fmt', 'yuv420p',
    #             '-color_range', '2',
    #             '-i', img,
    #             '-vf',
    #             f'scale={size}',
    #             '-y',
    #             out_path
    #         ]
        
    #     subprocess.run(ffmpeg_command)

    #     return out_path
    
    # def _resize_clips(self, clips, size):
    #     resize_paths = []
        
    #     for i, clip in enumerate(clips, 1):
    #         resize_out = os.path.join(utils.get_root_path(), 'temp', f'resize{i}.mp4')
    #         ffmpeg_command = [
    #             'ffmpeg',
    #             # '-hide_banner',
    #             # '-loglevel',
    #             # 'quiet',
    #             '-i', clip,
    #             '-vf',
    #             f'[0:v]scale={size},setsar=1[v0];',
    #             '-y',
    #             '-c:v', 'libx264',
    #             '-c:a', 'aac',
    #             '-strict', 'experimental',
    #             resize_out
    #         ]
    #         subprocess.run(ffmpeg_command)

    #         resize_paths.append(resize_out)

    #     return resize_paths



    def _fill_duration_randomly(self, files, folder):
        selected_files = []
        selected_files_duration = 0
        files_len = len(files)
        # Randomly select file from folder until target duration is met
        while selected_files_duration < self.target_duration:
            if len(files) > 0:
                selection = random.choice(files)
                selected_files.append(selection)
                files.remove(selection)
            else:
                selection = random.choice(selected_files)
                # Make sure a clip is not duplicated back-to-back, unless there is only one file in the folder
                while selection == selected_files[-1] and files_len != 1:
                    selection = random.choice(selected_files)

                selected_files.append(selection)

            # Get duration of selected file and add to duration of selections
            probe = ffmpeg.probe(os.path.join(folder, selection), show_entries='format=duration')
            file_duration = float(probe['format']['duration'])
            selected_files_duration += file_duration

        return selected_files
    
    def _select_random_files(self, folder, hasDuration=False):
        # Get all video file names in the specified folder
        files = [file for file in os.listdir(folder)]
        
        if len(files) == 0:
            return []
        if hasDuration:
            selected_files = self._fill_duration_randomly(files, folder)
        else:
            return random.choice(files)
       
        random_paths = [os.path.join(folder, file) for file in selected_files]

        return random_paths

    # def _get_random_transition(self):
    #     transitions = ['fade', 'wipeleft', 'wiperight','wipeup','wipedown','slideleft','slideright','slideup',
    #         'slidedown','circlecrop','rectcrop','distance','fadeblack','fadewhite','radial','smoothleft','smoothup','smoothdown',
    #         'circleopen','circleclose','vertopen','vertclose','horzopen','horzclose','dissolve','pixelize','diagtl','diagtr',
    #         'diagbl','diagbr','hlslice','hrslice','vuslice','vdslice','hblur','fadegrays','wipetl','wipetr','wipebl','wipebr',
    #         'squeezeh','squeezev','zoomin','fadefast','fadeslow','hrwind','vuwind','vdwind','coverleft','coverright',
    #         'coverup','coverdown','revealleft','revealright','revealup','revealdown'
    #     ]

    #     return random.choice(transitions)

    # def _create_transition_segment(self, clip1, clip2, duration, clip_length, idx):
    #     transition_out = os.path.join(utils.get_root_path(), 'temp', f'transition{idx}.mp4')

    #     transition = self._get_random_transition()
    #     ffmpeg.probe(clip1)
    #     ffmpeg.probe(clip2)
    #     # resized_clips = self._resize_clips([clip1, clip2], "576:1024")
    #     resized_clips = self._resize_clips([clip1, clip2], "720:1280")
    #     ffmpeg_command = [
    #         'ffmpeg',
    #         # '-hide_banner',
    #         # '-loglevel',
    #         # 'quiet',
    #         '-i', resized_clips[0],
    #         '-i', resized_clips[1],
    #         '-filter_complex',
    #         f'[0]settb=AVTB,fps=30[v0];[1]settb=AVTB,fps=30[v1]; [0:a]aformat=sample_rates=44100:channel_layouts=stereo[a0]; [1:a]aformat=sample_rates=44100:channel_layouts=stereo[a1]; [v0][v1]xfade=transition={transition}:duration={duration}:offset={clip_length - duration},format=yuv420p[vout]; [a0][a1]acrossfade=d=1[aout]',
    #         '-map', "[vout]",
    #         '-map', "[aout]",
    #         '-y',
    #         '-c:v', 'libx264',
    #         '-c:a', 'aac',
    #         '-strict', 'experimental',
    #         transition_out
    #     ]
    #     subprocess.run(ffmpeg_command)

    #     return transition_out

    # def _build_transition_inputstreams(self, clips):
    #     input_streams = []

    #     if len(clips) == 1:
    #         input_streams.append(ffmpeg.input(clips[0], ss=0))
    #     else: 
    #         for i, clip in enumerate(clips):

    #             if not self._has_audio(clip):
    #                 print("\n\n\n\n", clip, "is being silenced...")
    #                 clips[i] = self._insert_silent(clip)
    #             # clip_duration = min(clip_duration, this_duration)  # Use the minimum between clip duration and desired duration
    #             probe = ffmpeg.probe(clip, show_entries='format=duration')
    #             clip_duration = float(probe['format']['duration'])
    #             print(i, clip)
    #             print("duration:", clip_duration, "\n")
    #             if (i > 0):
    #                 probe = ffmpeg.probe(clips[i-1], show_entries='format=duration')
    #                 clip_duration = float(probe['format']['duration'])
    #                 transition_segment = self._create_transition_segment(clips[i-1], clips[i], 0.5, clip_duration, i)
    #                 if (i == len(clips) - 1):
    #                     clip_duration *= 2
                
    #                 input_stream = ffmpeg.input(transition_segment, ss=0, t=clip_duration)
    #                 input_streams.append(input_stream)

    #     return input_streams


    # def _add_watermark(self, img, video):
    #     watermark_out = os.path.join(utils.get_root_path(), 'temp', f'watermark_video.mp4')
    #     size = '300:180'
    #     img_resized = self._resize_img(img, size)
    #     ffmpeg_command = [
    #         'ffmpeg',
    #         # '-hide_banner',
    #         # '-loglevel',
    #         # 'quiet',
    #         '-i', video,
    #         '-i', img_resized,
    #         '-filter_complex',
    #         f'[1:v]format=rgba,colorchannelmixer=aa=0.5[overlay];[0:v][overlay]overlay=10:10[video]',
    #         '-map', '[video]',
    #         '-map', '0:a',
    #         '-c:v', 'libx264',
    #         '-c:a', 'aac',
    #         '-y',
    #         '-strict', 'experimental',
    #         watermark_out
    #     ]

        
    #     subprocess.run(ffmpeg_command)
    #     # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    #     # print(ffmpeg_command_str)
    #     return watermark_out
        
    # def _add_voice_over(self, video, voice):
    
    #     voice_out = os.path.join(utils.get_root_path(), 'temp', f'voice_video.mp4')
        
    #     ffmpeg_command = [
    #         'ffmpeg',
    #         '-hide_banner',
    #         '-loglevel',
    #         'quiet',
    #         '-i', video,
    #         '-i', voice,
    #         '-filter_complex',
    #         f"[0:a]volume=1.0[a0];[1:a]volume=3.5[a1];[a0][a1]amix=inputs=2[aout]",
    #         '-map', '0:v',
    #         '-map', '[aout]',
    #         '-c:v', 'copy',
    #         '-c:a', 'aac',
    #         '-y',
    #         '-strict', 'experimental',
    #         voice_out
    #     ]

        
    #     subprocess.run(ffmpeg_command)
    #     # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    #     # print(ffmpeg_command_str)
    #     return voice_out

    def _wrap_text(self, text, max_width):
        """
        Wrap text to fit within a maximum width.

        Parameters:
            text (str): The input text.
            max_width (int): The maximum width for each line.

        Returns:
            str: The wrapped text.
        """
        words = text.split()  # Split the text into words
        lines = []  # List to store lines of wrapped text
        current_line = ''  # Current line being constructed

        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:  # Check if adding the word exceeds max_width
                if current_line:  # If current_line is not empty, add a space before adding the word
                    current_line += ' '
                current_line += word
            else:
                lines.append(current_line)  # Add the current_line to lines
                current_line = word  # Start a new line with the current word

        if current_line:  # Add the remaining line
            lines.append(current_line)

        return '\n'.join(lines)  # Join the lines with newline characters
    
    # def _add_text(self, video):
    #     text_out = os.path.join(utils.get_root_path(), 'temp', f'text_video.mp4')
    #     font_style =  'font_ttfs/font.ttf'
    #     quote_wrapped = self.wrap_text(self.quote, 20)
    #     print("\n\n\n\n\nquote: ", quote_wrapped, "\n\n\n\n\n")
    #     ffmpeg_command = [
    #         'ffmpeg',
    #         # '-hide_banner',
    #         # '-loglevel',
    #         # 'quiet',
    #         '-i', video,
    #         '-filter_complex',
    #         f"drawtext=text='{quote_wrapped}':fontfile={self.font_style}:fontsize={self.font_size}:fontcolor=#000000:box=1:boxcolor=black@0.0:boxborderw=5:x=(W-text_w)/2:y=(H-text_h)/2:enable='between(t,0,5)'[text];[0:v][text]overlay=0:0",
    #         '-c:v', 'libx264',
    #         '-c:a', 'aac',
    #         '-y',
    #         '-strict', 'experimental',
    #         text_out
    #     ]

        
    #     subprocess.run(ffmpeg_command)
    #     # ffmpeg_command_str = ' '.join(map(str, ffmpeg_command))
    #     # print(ffmpeg_command_str)
    #     return text_out
    
    def render(self):
        
        # transitions_video = os.path.join(export_folder, 'output', 'final_video.mp4')

        start_time = time.time()
        # Build Video Streams
        video_clips = self._select_random_files(self.video_folder, True)
        audio_clips = self._select_random_files(self.audio_folder, True)
        # img = self._select_random_files(self.overlay_folder, False)
        # if len(img) > 0:
        #     # Select Image Overlay
        #     imgpath = os.path.join(utils.get_root_path(), self.overlay_folder, img)
        # else:
        #     imgpath = None
        print("\n\n\n\n\n Transitions render...")
        print(audio_clips)
        transitions_video = fmpgapi.build_transitions(video_clips, self.target_duration, self.fade_duration, '576x1024')
        
        if len(audio_clips) > 0:
            print("here")
            transitions_with_audio = fmpgapi.add_audio(transitions_video, audio_clips, self.target_duration)
        else:
            transitions_with_audio = transitions_video

        
        
        # transitions_video = os.path.join(utils.get_root_path(), 'temp',  'transitions_video.mp4' )

        # video_input_streams = self._build_transition_inputstreams(video_clips)

        # # Build Audio Streams
        # audio_clips = self.select_random_files(self.audio_folder, True)
        # audio_input_streams = []
        # for audio in audio_clips:
        #     audio_input_streams.append(ffmpeg.input(audio, ss=0))
        

        # output_options = {
        #     'c:v': 'libx264',
        #     'c:a': 'aac',
        #     'strict': 'experimental',
        #     # 'hide_banner': True,
        #     # 'loglevel': 'quiet',
        # }
        # if len(audio_input_streams) > 0:
        #     video = ffmpeg.concat(*video_input_streams, v=1, a=0)
        #     audio = ffmpeg.concat(*audio_input_streams, v=0, a=1)     
        
        # else:       
        #     video = ffmpeg.concat(*video_input_streams, v=1, a=0)
        #     audio = ffmpeg.concat(*video_input_streams, v=0, a=1)
        #     # ffmpeg.output(audio, 'test.mp4', t=self.target_duration, **output_options).run(overwrite_output=True)
        #     # probe = ffmpeg.probe('test.mp4', show_entries='format=duration')
        #     # print("duration: " , float(probe['format']['duration']))
        # ffmpeg.output(video, audio, transitions_video, t=self.target_duration, **output_options).run(overwrite_output=True)
        
        # logger = MyBarLogger()
        

        
        full_render = transitions_with_audio
        text_videopath = None
        
    
            
        if self.quote != '':
            voice_video = fmpgapi.add_voice_over(transitions_with_audio, self.voice)
            quote_wrapped = self._wrap_text(self.quote, 20)
            text_video = fmpgapi.add_text(voice_video, quote_wrapped, self.font_style, self.font_size)
            text_videopath = os.path.join(utils.get_root_path(), 'temp', text_video)
            full_render = text_videopath 
            
        # if imgpath:
        #     if text_videopath is not None:
        #         full_render = fmpgapi.add_watermark(imgpath, text_videopath)
        #     else: 
        #         full_render = fmpgapi.add_watermark(imgpath, transitions_video)
        if self.overlay_folder is not None:
            # Select Image Overlay
            img = self._select_random_files(self.overlay_folder, False)
            imgpath = os.path.join(utils.get_root_path(), self.overlay_folder, img)
            print("\n\n\n\n\n Watermark render...\n\n\n\n\n")
            if text_videopath is not None:
                full_render = fmpgapi.add_watermark(imgpath, text_videopath)
            else: 
                full_render = fmpgapi.add_watermark(imgpath, transitions_video)
            

        end_time = time.time()

        time_difference = end_time - start_time
        
        print("Success! Time taken:", time_difference)

        # data = open_json()
        # data["export"]["exported_videos"].append(transitions_video)
        # save_json(data)

        # st.toast(f"This video export took {int(time_difference)} seconds to export", icon="🚀")
        # st.write(f"This video export took {int(time_difference)} seconds to export")

        # average_exporting_speed = (i+1) * 3600 / duration_taken

        # st.success(f"Luxury Clips Created Successfully! With the speed {int(average_exporting_speed)} videos/hour.")

        # if logger.percentage == 100:
        #     st.video(transitions_video)

        final_video_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
        utils.move_file_to_output_dir(full_render, final_video_filename)
        # Clean up temp file
        # utils.clean_temp()
        
        
