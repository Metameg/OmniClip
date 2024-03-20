from flask import Blueprint, request, flash, render_template, jsonify

from app.tools import utilities
import os

blueprint = Blueprint('media_uploader', __name__)

@blueprint.route('/upload-media', methods=['POST'])
def upload_media():
    
    files = request.files.getlist('files[]')

    # Process each uploaded file
    mediapaths = []
    upload_dirs = []
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

    for file in files:

        sanitized_filename = utilities.sanitize_filename(file.filename)
        file_path = utilities.truncate(sanitized_filename, 18)

        if utilities.is_video_file(file.filename):
            upload_dir =  'video_uploads'
            tag_type = 'video'
            video_content = render_template(template, upload_dirs=[upload_dir], mediapaths=[file_path], tag_type=tag_type)
            html_data[1]["videos"] += video_content

        elif utilities.is_audio_file(file.filename):
            upload_dir = 'audio_uploads'
            tag_type = 'audio'
            audio_content = render_template(template, upload_dirs=[upload_dir], mediapaths=[file_path], tag_type=tag_type)
            html_data[2]["audios"] += audio_content

        elif utilities.is_image_file(file.filename):
            upload_dir =  'watermark_uploads'
            tag_type = 'img'
            image_content = render_template(template, upload_dirs=[upload_dir], mediapaths=[file_path], tag_type=tag_type)
            html_data[3]["images"] += image_content
            
        else:
            return "Error! Only upload media files."

        
        
        # Save the file to appropriate directory
        file.save(os.path.join(upload_dir, file_path))
        mediapaths.append(file_path)
        upload_dirs.append(upload_dir)

        # Add file to the all media html data
        aggregate_content = render_template(template, upload_dirs=upload_dirs, mediapaths=mediapaths, tag_type=tag_type)
        html_data[0]["allMedia"] = aggregate_content

    
    return jsonify(html_data)
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    


# @blueprint.route('/retrieve-videos')
# def retrieve_videos():
