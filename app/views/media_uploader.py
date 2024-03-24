from flask import Blueprint, request, jsonify, session
from app.tools import helpers, database
from app.tools.utilities import get_file_size, get_root_path, truncate, sanitize_filename, get_media_dir
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db
import os

blueprint = Blueprint('media_uploader', __name__)

@blueprint.route('/upload-media', methods=['POST'])
def upload_media():
    files = request.files.getlist('files[]')

    

    if "user" in session:
        username = session["user"]
        user_id = database.retrieve(User, username=username).id
        media_dir = get_media_dir(username)

        
    else:
        user_id = None
        media_dir = os.path.join(get_root_path(), 'temp', 'guest')

    file_paths = []
    for file in files:
        filename = truncate(sanitize_filename(file.filename), 18)
        path = os.path.join(media_dir, filename)
        file_paths.append(path)
        file.save(path)

    if user_id:
        for path in file_paths:
            db_file = Media.query.filter_by(path=path).first()

            # If file is not in userData, add file to db and userData
            if db_file is None:
                file_size = get_file_size(file)
                database.create(db, Media, user_id=user_id, path=path, filename=filename, size=file_size)

    html_data = helpers.build_media_html(file_paths)
    return jsonify(html_data)
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    
@blueprint.route('/retrieve-user-media')
def retrieve_medias():
    
    if "user" in session:
        username = session["user"]
        print("username: ", username)
        media_dir = get_media_dir(username)
        print("directory: ", media_dir)
        # filenames = os.listdir(media_dir)
        
        # for filename in filenames:
        #     path = os.path.join(media_dir, filename)
        #     file_paths.append(path) 
    
        medias = database.retrieve_from_join(db, User, Media, username)
        for p in medias:
            print("media: ", p)
        file_paths = [database.retrieve(Media, media_id=media.media_id).path for media in medias]
        for p in file_paths:
            print("path: ", p)
        s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]
        for p in s3_urls:
            print(p)
    else:
        html_data = [
            {"allMedia": "" },
            {"videos": ""},
            {"audios": ""},
            {"images": ""}
        ]   
        return jsonify(html_data)
    
    html_data = helpers.build_media_html(file_paths)
    print("\n data:\n", html_data)

    return jsonify(html_data)

