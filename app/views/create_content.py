import json
from datetime import datetime, timezone
from flask import Blueprint, request, render_template, session
from app.extensions import db, csrf
from app.models.User import User
from app.tools.utilities import generate_videos, get_root_path, decode_path, get_media_dir, sanitize_filename
from app.tools.helpers import classify_custom_upload_files
from app.tools import database
from app.services.AutoEditor import AutoEditor
import os
from app.models.Render import Render

blueprint = Blueprint('create_content', __name__)


@blueprint.route('/create-content', methods=['GET'])
def create_content():
    with open('voices.json', 'r') as f:
        voices = json.load(f)['voices']
    
    return render_template("pages/create-content.html", voices=voices)


@blueprint.route('/create-content', methods=['POST'])
def render():
    # Validate the CSRF token
    csrf.protect()

    if "user" in session:
        username = session["user"]
        # user_id = database.retrieve(User, username=username).id
        outpath = os.path.join(get_media_dir(username), 'renders')

    else:
        user_id = None
        outpath = os.path.join(get_root_path(), '..', 'userData', 'guest')

    form_data = request.get_json()

    for key, value in form_data.items():
        print(f"{key}: {value}")

    selected_media = form_data['selectedMedia[]']
    if isinstance(selected_media, str):
        selected_media = [form_data['selectedMedia[]']]
    
    uploaded_files = classify_custom_upload_files(selected_media)

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
    voice = os.path.join('static', 'voices', form_data['voice'] + '.mp3')
    numvideos = int(form_data['numvideos'])

    
    # Render the Video
    editor = AutoEditor(uploaded_files['video_uploads'], uploaded_files['audio_uploads'], 
                    uploaded_files['watermark_uploads'], fade_duration, target_duration, 
                    'freedom', font_size, text_primary_color, text_outline_color, 
                    isBold, isItalic, isUnderline, 
                    alignment, watermark_opacity, output_dir=outpath,
                    quote=quote_val, voice=voice, subtitle_ass=True)

    video_paths = generate_videos(editor, numvideos, outpath)
    upload_renders(video_paths, aspect_ratio)

    # Add videos to Renders table
    return render_template('partials/video-container.html', user_dir=outpath, videopaths=video_paths)


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