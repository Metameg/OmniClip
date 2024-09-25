import os
from datetime import datetime
import time
import random
from app.tools import utilities
from . import ffmpeg_commands as fmpgapi
from app.services.transcribe_subtitles import transcribe_subtitles
from app.services.shotstacktts import generate_tts
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
    def __init__(self, video_folder, audio_folder, 
                 overlay_folder, fade_duration, target_duration, 
                 font_name, font_size, text_primary_color, text_outline_color,
                 isBold, isItalic, isUnderline, alignment,
                 watermark_opacity, output_dir='guest', quote=None, voice=None, subtitle_ass=True):
        
        self.fade_duration = fade_duration
        self.target_duration = target_duration
        self.video_folder = video_folder
        self.audio_folder = audio_folder
        self.overlay_folder = overlay_folder
        self.watermark_opacity = watermark_opacity
        self.export_folder = output_dir
        self.quote = quote
        self.voice = voice
        self.subtitle_ass = subtitle_ass

        self.style_options = ['font_ttfs/' + font_name + '.ttf', font_size,
                                 text_primary_color, text_outline_color, 
                                 isBold, isItalic, isUnderline,
                                 alignment]

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
            # probe = ffmpeg.probe(os.path.join(folder, selection), show_entries='format=duration')
            # selection_path = os.path.join(folder, selection)
            print("selection", selection, type(selection))
            file_duration = fmpgapi.get_length(selection)
            # file_duration = fmpgapi.get_length(selection_path)
            selected_files_duration += file_duration
            
            print("file duration: ", file_duration)
            print("selected_files_duration: ", selected_files_duration)
            

        return selected_files
    
    def _select_random_files(self, folder, hasDuration=False):
        # Get all video file names in the specified folder
        files = [file for file in folder]
        # files = [file for file in os.listdir(folder)]
        
        if len(files) == 0:
            return []
        if hasDuration:
            selected_files = self._fill_duration_randomly(files, folder)
        else:
            return random.choice(files)
       
        # random_paths = [os.path.join(folder, file) for file in selected_files]
        # for r in random_paths:
        #     print(r, '\n')
            
        return selected_files


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
    
    
    def render(self):
        
        # transitions_video = os.path.join(export_folder, 'output', 'final_video.mp4')

        start_time = time.time()
        
        cleaned_videos = utilities.decode_and_clean_paths(self.video_folder)
        video_clips = self._select_random_files(cleaned_videos, True)
        
        if self.audio_folder is not None:
            cleaned_audios = utilities.decode_and_clean_paths(self.audio_folder)
            audio_clips = self._select_random_files(cleaned_audios, True)
        # Randomly Select Video Clips 
        
        # Create Transition Segments
        print("\n\n\n\n\n Transitions render...")
        transitions_video = fmpgapi.build_transitions(video_clips, self.target_duration, self.fade_duration, '720:1280')
        
        if self.audio_folder is not None and len(audio_clips) > 0:
            print("\n\n\n audio found!\n\n\n")
            transitions_with_audio = fmpgapi.add_audio(transitions_video, audio_clips, self.target_duration)
        else:
            print("\n\n\n audio not found!\n\n\n")
            transitions_with_audio = transitions_video
  
        # logger = MyBarLogger()

        full_render = transitions_with_audio
        text_videopath = None
        
    
            
        if self.quote != '':
            self.voice = generate_tts(self.quote, 'Joey')
            voice_video = fmpgapi.add_voice_over(transitions_with_audio, self.voice)
            if self.subtitle_ass:
                
                
                transcribe_subtitles(self.voice, self.style_options)
                ass_file = 'temp/subtitles.ass'
                text_video = fmpgapi.add_text(voice_video, ass_file=ass_file)
            else:
                quote_wrapped = self._wrap_text(self.quote, 20)
                text_video = fmpgapi.add_text(voice_video, self.style_options[0], self.style_options[1], quote=quote_wrapped)
                

            text_videopath = os.path.join(utilities.get_root_path(), 'temp', text_video)
            full_render = text_videopath 
            

        if self.overlay_folder is not None and len(self.overlay_folder) > 0:
            cleaned_overlays = utilities.decode_and_clean_paths(self.overlay_folder)
            # Select Image Overlay
            img = self._select_random_files(cleaned_overlays, False)
            # imgpath = os.path.join(utilities.get_root_path(), self.overlay_folder, img)
            print("\n\n\n\n\n Watermark render...\n\n\n\n\n")
            if text_videopath is not None:
                full_render = fmpgapi.add_watermark(img, text_videopath, self.watermark_opacity)
                # full_render = fmpgapi.add_watermark(imgpath, text_videopath)
            else: 
                full_render = fmpgapi.add_watermark(img, full_render, self.watermark_opacity)
                # full_render = fmpgapi.add_watermark(imgpath, transitions_video)
            

        end_time = time.time()

        time_difference = end_time - start_time
        
        print("Success! Time taken:", time_difference)
        print(f"full filename {full_render}")
        final_video_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".mp4"
        utilities.move_file_to_output_dir(self.export_folder, full_render, final_video_filename)
        # Clean up temp file
        # utilities.clean_temp()
        
        
