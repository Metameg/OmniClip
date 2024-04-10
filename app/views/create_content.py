import json
from flask import Blueprint, request, flash, render_template
from app.extensions import db, csrf
from app.models.User import User
from app.tools.utilities import generate_videos, get_root_path, decode_path
from app.tools.helpers import classify_file_type
from app.services.AutoEditor import AutoEditor
import os

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
    
    form_data = request.get_json()

    for key, value in form_data.items():
        print(f"{key}: {value}")

    selected_media = form_data['selectedMedia[]']
    if isinstance(selected_media, str):
        selected_media = [form_data['selectedMedia[]']]
    
    has_video = False
    video_uploads = []
    audio_uploads = []
    watermark_uploads = []

    for path in selected_media:
        path = decode_path(path)
        print(type(path), path)
        if classify_file_type(path) == 'video':
            has_video = True
            video_uploads.append(path)
        elif classify_file_type(path) == 'audio':
            audio_uploads.append(path)
        elif classify_file_type(path) == 'img':
            watermark_uploads.append(path)

    
    outpath = 'output'
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
    # aspect_ratio = form_data['aspectRatio']
    alignment = int(form_data['subtitleAlignment'])
    watermark_opacity = form_data['watermarkOpacity']
    quote_val = form_data['quoteVal']
    voice = os.path.join('static', 'voices', form_data['voice'] + '.mp3')
    numvideos = int(form_data['numvideos'])

    
    editor = AutoEditor(outpath, video_uploads, audio_uploads, 
                        watermark_uploads, fade_duration, target_duration, 
                        'freedom', font_size, text_primary_color, text_outline_color, 
                        isBold, isItalic, isUnderline, 
                        alignment, watermark_opacity,
                        quote=quote_val, voice=voice, subtitle_ass=True)
    
    videopaths = generate_videos(editor, numvideos)

    return render_template('partials/video-container.html', videopaths=videopaths)

@blueprint.route('/upload-media/<int:id>', methods=['GET', 'POST'])
def upload_media(id):
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.favorite_color = request.form['favorite_color']

        try:
            db.session.commit()
            flash("User Updated Successfully!")
            return render_template("update.html", user=user)
        except:
            flash("Error! Problem...Try Again")
            return render_template("update.html", user=user)

    else:
        return render_template("uploads_grid.html", user=user)