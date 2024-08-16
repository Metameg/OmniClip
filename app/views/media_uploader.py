from flask import Blueprint, request, jsonify, session
from app.tools import helpers, database, utilities
from app.tools.utilities import get_file_size, get_root_path, sanitize_filename, get_media_dir, split_filename
from app.models.User import  User
from app.models.Media import  Media
from app.extensions import db
import os, urllib

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
    media_files = os.listdir(media_dir)

    for file in files:
        filename = sanitize_filename(file.filename)
        path = os.path.join(media_dir, filename)
        
        if helpers.classify_file_type(path) == 'unknown':
            print("Unknown file type in one or more of your files. Only upload media files.")
            break

        if filename not in media_files:
            file_paths.append(path)
            file.save(path)
        else:
            copyidx = helpers.get_num_copies(filename, media_files)
            base, extension = split_filename(filename)
            filename = f"{base}({copyidx}){extension}"
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
        medias = database.retrieve_from_join(db, User, Media, username)
        file_paths = [database.retrieve(Media, media_id=media.media_id).path for media in medias]
 
        s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]
   
    else:
        html_data = [
            {"allMedia": "" },
            {"videos": ""},
            {"audios": ""},
            {"images": ""}
        ]   
        return jsonify(html_data)
    
    html_data = helpers.build_media_html(file_paths)

    return jsonify(html_data)

@blueprint.route('/remove-user-media/<path:path>', methods=['POST'])
def remove_media(path):
    file_paths = []
    path = urllib.parse.unquote(path)
    path = path.replace('/', os.path.sep).replace('\\', os.path.sep)
    if os.name == 'posix' and not path.startswith('/'):
        path = '/' + path

    if "user" in session:
        username = session["user"]  
        path = path.replace('/', os.path.sep)

        database.remove(db, Media, path)
        if (os.path.exists(path)):
            os.remove(path)

        s3_urls = [f"https://<bucket_name>.s3.amazonaws.com/{file_path}" for file_path in file_paths]

    else:
        if (os.path.exists(path)):
            os.remove(path)
        guest_dir = os.path.join(get_root_path(), 'temp', 'guest')
        for filename in os.listdir(guest_dir):
            # Join directory path with each file name to get the full path
            file_path = os.path.join(guest_dir, filename)
            
            # Check if the path points to a file (and not a directory)
            if os.path.isfile(file_path):
                # Append the full path to the list
                file_paths.append(file_path)
    
    html_data = "data removed"
    # html_data = helpers.build_media_html(file_paths)

    return jsonify(html_data)

@blueprint.route('/remove-guest-media', methods=['GET'])
def remove_guest_media():
    utilities.remove_guest_temp_files()

    return ('', 204)