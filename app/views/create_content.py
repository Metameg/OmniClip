import json
from datetime import datetime
from flask import Blueprint, request, render_template, session, jsonify, current_app
from app.extensions import db, csrf
from app.models.User import User
from app.tools.utilities import generate_videos, get_root_path, get_media_dir, sanitize_filename
from app.tools.helpers import classify_custom_upload_files, get_num_user_renders
from app.tools import database
from app.services.AutoEditor import AutoEditor
import os
from app.models.Render import Render

blueprint = Blueprint('create_content', __name__)


@blueprint.route('/create-content', methods=['GET'])
def create_content():
    voices_path = os.path.join(current_app.root_path, 'static', 'voices.json')
    with open(voices_path, 'r') as f:
        voices = json.load(f)['voices']
    
    return render_template("pages/create-content.html", voices=voices)

@blueprint.route('/create-content', methods=['POST'])
def render():
    # Validate the CSRF token
    csrf.protect()

    MAX_RENDERS_ALLOWED = 5

    if "user" in session:
        username = session["user"]
        outpath = os.path.join(get_media_dir(username), 'renders')
        user_dir = username

    else:
        user_id = None
        outpath = os.path.join(get_media_dir('guest'), 'renders')
        user_dir = 'guest'

    # Get form data from request
    form_data = request.get_json()

    # for key, value in form_data.items():
    #     print(f"{key}: {value}")


    # Handle uploaded files if they exist, otherwise use a clippack
    if 'selectedMedia[]' in form_data.keys():
        selected_media = form_data['selectedMedia[]']
        if isinstance(selected_media, str):
            selected_media = [form_data['selectedMedia[]']]
    
        uploaded_files = classify_custom_upload_files(selected_media)
        video_files = uploaded_files['video_uploads']
        audio_files = uploaded_files['audio_uploads']
        watermark_files = uploaded_files['watermark_uploads']
    else:
        clippack = form_data['clippack']
        clippack_path = os.path.join(get_root_path(), 'static', 'clippacks', clippack)
        video_files = [os.path.normpath(str(clippack_path + os.sep + f)) for f in os.listdir(clippack_path) if f.endswith(('.mp4'))]

        audio_files = None
        watermark_files = None


    # Store Request Data
    fade_duration = float(form_data['fadeoutDuration'])
    target_duration = float(form_data['totalLength'])
    font_name = form_data['fontName']
    font_size = int(form_data['fontSize'])
    text_primary_color = form_data['primaryColor']
    try:
        text_outline_color = form_data['outlineColor']
    except Exception:
        text_outline_color = '#00000000'
    isBold = form_data['isBold']
    isItalic = form_data['isItalic']
    isUnderline = form_data['isUnderline']
    aspect_ratio = form_data['aspectRatio']
    alignment = int(form_data['subtitleAlignment'])
    watermark_opacity = form_data['watermarkOpacity']
    quote_val = form_data['quoteVal']
    voice = form_data['voice']
    numvideos = int(form_data['numvideos'])


    # Check to see if there are too many renders stored in userData
    num_user_renders = get_num_user_renders(outpath)
    if num_user_renders + numvideos > MAX_RENDERS_ALLOWED:
        return jsonify('Cannot create more renders. Max allowed (5) reached. Please delete some renders from profile to make room for more.'), 413 
    

    # Render the Video
    editor = AutoEditor(video_files, audio_files, 
                    watermark_files, fade_duration, target_duration, 
                    font_name, font_size, text_primary_color, text_outline_color, 
                    isBold, isItalic, isUnderline, 
                    alignment, watermark_opacity, output_dir=outpath,
                    quote=quote_val, voice=voice, subtitle_ass=True)

    video_paths = generate_videos(editor, numvideos, outpath)
    upload_renders(video_paths, aspect_ratio)
    
    # Add videos to Renders table
    return render_template('partials/video-container.html', user_dir=user_dir, videopaths=video_paths)
    


def upload_renders(render_paths, aspect_ratio):
    if "user" in session:
        username = session["user"]
        user_id = database.retrieve(User, username=username).id
        media_dir = os.path.join(get_media_dir(username), 'renders')
        # media_dir = os.path.join(get_root_path(), 'output')
        for path in render_paths:
            filename = sanitize_filename(path)
            path = os.path.join(media_dir, filename)
            duration = 0

            
            database.create(db, 
                            Render, 
                            user_id=user_id, 
                            path=path, 
                            duration=duration, 
                            timestamp=datetime.now(),
                            aspect_ratio=aspect_ratio, 
                            filename=filename)