from flask import Blueprint, request, flash, render_template, jsonify
from app import db
from app.tools import utilities
import os

blueprint = Blueprint('media_uploader', __name__)

@blueprint.route('/upload-media', methods=['POST'])
def upload_media():
    
    files = request.files.getlist('files[]')

    # Process each uploaded file
    mediapaths = []
    upload_dirs = []
    for file in files:

        sanitized_filename = utilities.sanitize_filename(file.filename)

        if utilities.is_video_file(file.filename):
            upload_dir =  'video_uploads'

        elif utilities.is_audio_file(file.filename):
            upload_dir = 'audio_uploads'

        elif utilities.is_image_file(file.filename):
            upload_dir =  'watermark_uploads'
            
        else:
            return "Error! Only upload media files."

        file_path = sanitized_filename
        print(file_path)
        # Save the file to appropriate directory
        file.save(os.path.join(upload_dir, file_path))
        mediapaths.append(file_path)
        upload_dirs.append(upload_dir)

    # Respond with the list of file names
    return render_template('partials/media-uploads.html', upload_dirs=upload_dirs, mediapaths=mediapaths)
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    

@blueprint.route('/category', methods=['POST'])
def generate_quote_from_category():
    print("category selected")
    json_data = request.get_json()
    category = json_data['category']
    is_same_as_clippack = json_data['sameCategoryBln']
    clippackCategory = json_data['clippack']

    print("category:", category)
    print("bln:", is_same_as_clippack)
    print("clippack:", clippackCategory)
    print(f"category submit pressed. {category}")
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()

    if is_same_as_clippack == 'true':
        res = clippackCategory
    else:
        res = category
    
    return jsonify(res)