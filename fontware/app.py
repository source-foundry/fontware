import os
from secrets import token_urlsafe

from flask import Flask, render_template, request, send_from_directory
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect, CSRFError

from fontTools.ttLib import TTFont

app = Flask(__name__)

# ======================================
#
# Configuration
#
# ======================================

BASEDIR = os.path.abspath(os.path.dirname(__file__))
UPLOADS_DIR = os.path.join(BASEDIR, "uploads")

if not os.path.isdir(UPLOADS_DIR):
    os.mkdir(UPLOADS_DIR)

SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("No secret key set for Flask application")

app.config.update(
    UPLOAD_DIR=os.path.join(UPLOADS_DIR),
    # key for CSRF protection
    SECRET_KEY=SECRET_KEY,
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE=".ttf, .otf",
    DROPZONE_MAX_FILE_SIZE=5,
    DROPZONE_MAX_FILES=1,
    DROPZONE_ENABLE_CSRF=True,  # enable CSRF protection
)


dropzone = Dropzone(app)
csrf = CSRFProtect(app)  # initialize CSRFProtect

UPLOAD_RND_DIR = "x"


# ======================================
#
# Route Handling
#
# ======================================


@app.route("/", methods=["POST", "GET"])
def upload():
    global UPLOAD_RND_DIR
    if request.method == "POST":
        f = request.files.get("file")
        filepath = os.path.join(app.config["UPLOAD_DIR"], UPLOAD_RND_DIR, f.filename)
        tt = TTFont(f)
        name = tt["name"]
        tt.save(filepath)
    else:
        UPLOAD_RND_DIR = token_urlsafe(16)
        os.mkdir(os.path.join(app.config["UPLOAD_DIR"], UPLOAD_RND_DIR))

    return render_template("index2.html", random_dir=UPLOAD_RND_DIR)


@app.route("/push-files/<random_dir>")
def push_files(random_dir):
    font_dir = os.path.join(app.config["UPLOAD_DIR"], random_dir)
    for file_name in os.listdir(font_dir):
        if file_name.endswith(".otf") or file.endswith(".ttf"):
            return send_from_directory(font_dir, file_name, as_attachment=True)


# ======================================
#
# Error Handling
#
# ======================================

# handle CSRF error
@app.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400


if __name__ == "__main__":
    app.run(debug=False)
