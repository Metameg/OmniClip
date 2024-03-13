import json
from flask import Blueprint, request, flash, render_template
from app import db, csrf
from app.models.Users import Users
from app.tools.utilities import generate_videos, upload_files
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
    print("here")
    # Validate the CSRF token
    csrf.protect()
    # json_data = request.get_json()
    # print(json_data)
    # if request.form.get("action") == "formData":
    videos = request.files.getlist('mediaPath')
    print(videos)
    audios = request.files.getlist('audioPath')
    print(audios)
    watermarks = request.files.getlist('watermarkPath')
    print(watermarks)
    form_data = request.form
    print(len(videos), len(audios), len(watermarks))
    # clippack_category = form_data['clippack']

    for key, value in form_data.items():
        print(f"{key}: {value}")

    # if import videos was disabled, set video upload directory to appropriate clippack category
    if len(videos) == 0:
        # video_uploads_dir = os.path.join('clippack_categories', clippack_category)
        video_uploads_dir = 'video_uploads'
    else:
        if videos[0].filename == '':
            video_uploads_dir = 'video_uploads'
        else:
            video_uploads_dir = 'video_uploads'
            upload_files(videos, video_uploads_dir)

    if len(audios) == 0:
        audio_uploads_dir = 'audio_uploads'

    elif  audios[0].filename != '':
        upload_files(audios, 'audio_uploads')

    if len(watermarks) == 0:
        watermark_uploads_dir = None
    else:
        if  watermarks[0].filename == '':
            watermark_uploads_dir = None
        else:
            watermark_uploads_dir = 'watermark_uploads'
            upload_files(watermarks, 'watermark_uploads')
        

    
    outpath = 'output'
    audio_uploads_dir = 'audio_uploads'
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

    editor = AutoEditor(outpath, video_uploads_dir, audio_uploads_dir, 
                        watermark_uploads_dir, fade_duration, target_duration, 
                        'freedom', font_size, text_primary_color, text_outline_color, 
                        isBold, isItalic, isUnderline, 
                        alignment, watermark_opacity,
                        quote=quote_val, voice=voice, subtitle_ass=True)
    
    videopaths = generate_videos(editor, numvideos)

    return render_template('partials/video-container.html', videopaths=videopaths)

@blueprint.route('/upload-media/<int:id>', methods=['GET', 'POST'])
def upload_media(id):
    user = Users.query.get_or_404(id)
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