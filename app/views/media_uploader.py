from flask import Blueprint, request, jsonify, session
from app.tools import helpers, database
from app.tools.utilities import get_file_size, get_root_path, truncate, sanitize_filename
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db
import os

blueprint = Blueprint('media_uploader', __name__)

@blueprint.route('/upload-media', methods=['POST'])
def upload_media():
    files = request.files.getlist('files[]')
    html_data = helpers.build_media_html(files)

    if "user" in session:
        username = session["user"]
        user_id = database.retrieve(User, username=username).id
        media_dir = os.path.join(get_root_path(), '..', 'userData', username)
    else:
        user_id = None

    if user_id:
        for file in files:
            if file.filename not in os.listdir(media_dir):

                filename = truncate(sanitize_filename(file.filename), 18)
                path = os.path.join(media_dir, filename)
                file.save(path)

            file_size = get_file_size(file)
            database.create(db, Media, user_id=user_id, path=path, filename=filename, size=file_size)

    
    return jsonify(html_data)
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    
@blueprint.route('/retrieve-user-media')
def retrieve_medias():
    
    if "user" in session:
        username = session["user"]
    else:
        data = [
            {"allMedia": "" },
            {"videos": ""},
            {"audios": ""},
            {"images": ""}
        ]   
        return jsonify(data)
    
    data = database.retrieve_from_join(db, User, Media, username)
    print(data)
    html_data = helpers.build_media_html(data)

    return html_data

    return jsonify(data)
