from flask import Blueprint, request, jsonify, session
from app.tools import helpers, database
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db

blueprint = Blueprint('media_uploader', __name__)

@blueprint.route('/upload-media', methods=['POST'])
def upload_media():
    if "user" in session:
        username = session["user"]
        user_id = database.retrieve(User, username=username).id
    else:
        user_id = None

    files = request.files.getlist('files[]')
    if user_id:
        for file in files:
            database.create(db, Media, user_id=user_id, filename=file.filename)

    html_data = helpers.build_media_html(files)
    
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
    html_data = helpers.build_media_html(data)

    return html_data

    return jsonify(data)
