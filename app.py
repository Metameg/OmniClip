import json
import os
from dotenv import load_dotenv
from flask import Flask, render_template, flash, request, jsonify, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from python.AutoEditor import AutoEditor
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import python.utilities

app = Flask(__name__)
load_dotenv()
mysql_pwd = os.getenv('MYSQL_PWD')
flask_key = os.getenv('FLASK_KEY')
# Config MySQL database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:' + mysql_pwd + '@localhost/my_users'
# Config CSRF for form
app.config['SECRET_KEY'] = flask_key
csrf = CSRFProtect(app)

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(120), nullable=False, unique=True)
#     favorite_color = db.Column(db.String(120))
#     date_added = db.Column(db.DateTime, default=datetime.utcnow())

    # def __repr__(self):
    #     return '<Name %r>' % self.name

        # with app.app_context():
        #     db.create_all()

# progress_percentage = 0

# Create a Form Class
# class EmailForm(FlaskForm):
#     email = StringField("Email:", validators=[DataRequired()])
#     submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite Color")
    submit = SubmitField("Submit")


# @app.route('/user/add', methods=['GET', 'POST'])
#def add_user():
  #  name = None
  #  form = UserForm()
  #  if form.validate_on_submit():
  #       user = Users.query.filter_by(email=form.email.data).first()
  #       if user is None:
  #           user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color)
  #           db.session.add(user)
  #           db.session.commit()
  #       name = form.name.data
  #       form.name.data = ''
  #       form.email.data = ''
  #       form.favorite_color.data = ''
  #       flash("User Added!")
  #   our_users = Users.query.order_by(Users.date_added)
  #   return render_template("add_user.html", form=form, name=name, our_users=our_users)

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     form = UserForm()
#     name_to_update = Users.query.get_or_404(id)
#     if request.method == 'POST':
#         name_to_update.name = request.form['name']
#         name_to_update.email = request.form['email']
#         name_to_update.favorite_color = request.form['favorite_color']
#
#         try:
#             db.session.commit()
#             flash("User Updated Successfully!")
#             return render_template("update.html", form=form, name_to_update=name_to_update)
#         except:
#             flash("Error! Problem...Try Again")
#             return render_template("update.html", form=form, name_to_update=name_to_update)
#
#     else:
#         return render_template("update.html", form=form, name_to_update=name_to_update)





@app.route('/')
def index():
    stuff = "This is <strong>Bold</strong>"
    return render_template("pages/home.html", stuff=stuff)

@app.route('/about')
def about():
    return render_template("pages/about.html")




@app.route('/affiliate-program/dashboard')
def affiliate_dashboard():
    return render_template("pages/affiliate/affiliate-dashboard.html")

@app.route('/affiliate-program/sign-up')
def affiliate_signup():
    return render_template("pages/affiliate/affiliate-sign-up.html")

@app.route('/affiliate-program/about')
def affiliate_about():
    return render_template("pages/affiliate/affiliate-about.html")


@app.route('/settings')
def settings():
    return render_template("pages/settings.html")













@app.route('/pricing')
def pricing():
    return render_template("pages/pricing.html")

@app.route('/checkout')
def checkout():
    return render_template("pages/checkout.html")

@app.route('/profile/<name>')
def user(name):
    return render_template("pages/profile.html", user_name=name)



def sanitize_filename(filename):
    # Replace spaces with underscores and remove other special characters
    return ''.join(c if c.isalnum() or c in ['.', '_'] else '_' for c in filename)

def upload_files(files, export_folder):

    for file in files:
        sanitized_filename = sanitize_filename(file.filename)
       
        
        # Save the file to the 'uploads' directory with the sanitized filename
        file.save(os.path.join(export_folder, sanitized_filename))
        # print(test_jpeg(file.getvalue()))
            
            
@app.route('/quote-generator/gpt', methods=['POST'])
def generate_quote_gpt():
    from python.GPT import QuoteGenerator
    print("gpt selected")
    json_data = request.get_json()
    prompt = json_data["prompt"]
    print(f"Quote submit pressed. {prompt}")
    generator = QuoteGenerator(prompt)
    # prompt = request.get_json()["prompt"]
    res = generator.generate()
    # threading.Thread(target=simulate_time_consuming_process, args=()).start()
    
    return jsonify(res)

@app.route('/quote-generator/category', methods=['POST'])
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

@app.route('/create-content', methods=['GET'])
def create_content():
    # csrf_token = csrf._get_csrf_token()
    with open('voices.json', 'r') as f:
        voices = json.load(f)['voices']
    
    return render_template("pages/create-content.html", voices=voices)


@app.route('/create-content', methods=['POST'])
def render():
    print("here")
    # Validate the CSRF token
    csrf.protect()
    # json_data = request.get_json()
    # print(json_data)
    # if request.form.get("action") == "formData":
    videos = request.files.getlist('clippackPath')
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

    if  audios[0].filename != '':
        upload_files(audios, 'audio_uploads')

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
    try:
        text_back_color = form_data['backColor'] 
    except Exception:
        text_back_color = '#00000000'

    isBold = form_data['isBold']
    isItalic = form_data['isItalic']
    isUnderline = form_data['isUnderline']
    text_posX = form_data['positionX']
    text_posY = form_data['positionY']
    aspect_ratio = form_data['aspectRatio']
    watermark_opacity = form_data['watermarkOpacity']
    quote_val = form_data['quoteVal']
    voice = os.path.join('static', 'voices', form_data['voice'] + '.mp3')
    numvideos = int(form_data['numvideos'])
    
    editor = AutoEditor(outpath, video_uploads_dir, audio_uploads_dir, 
                        watermark_uploads_dir, fade_duration, target_duration, 
                        'freedom', font_size, text_primary_color, text_outline_color, 
                        text_back_color, isBold, isItalic, isUnderline, 
                        text_posX, text_posY, aspect_ratio, watermark_opacity,
                        quote=quote_val, voice=voice, subtitle_ass=True)
    videopaths = generate_videos(editor, numvideos)

    return render_template('partials/video-container.html', videopaths=videopaths)

# def simulate_time_consuming_process():
#     global progress_percentage
#     for _ in range(10):  # Simulate 10 steps of the process
#         time.sleep(1)  # Simulate some time-consuming task
#         progress_percentage += 10  # Update progress

#     # return jsonify({'htmlresponse': render_template('response.html')})
#     # progress_percentage = 0  # Reset progress after completion


def generate_videos(editor, numvideos):
    videos = []
    for _ in range(numvideos):
        # thread = threading.Thread(target=render_video, args=(editor,))
        # thread.start()
        # thread.join()
        editor.render()
        videopath = sorted(os.listdir('output'))[-1]
        videos.append(videopath)

    return videos

# @app.route('/get_progress')
# def get_progress():
#     return str(progress_percentage)
    
@app.route('/output/<filename>')
def serve_output(filename):
    return send_from_directory('output', filename)

@app.route('/loading_container_partial', methods=['GET'])
def loading_container_partial():
    return render_template("partials/loading-container.html")

# @app.route('/email', methods=['GET', 'POST'])
# def email():
#     email = None
#     form = EmailForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         form.email.data = ''
#         flash("Form Submitted Successfully.")
        
#     return render_template("email.html", email=email, form=form)

@app.route('/login')
def login():
    return render_template("pages/login.html")


# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("pages/404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("pages/500.html"), 500

if __name__ == '__main__':
    app.run(debug=True)
    