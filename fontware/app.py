import os

from flask import Flask, render_template, request
from flask_dropzone import Dropzone
from flask_wtf.csrf import CSRFProtect, CSRFError

from fontTools.ttLib import TTFont

app = Flask(__name__)

SECRET_KEY = os.environ.get("SECRET_KEY", default=None)
if not SECRET_KEY:
    raise ValueError("No secret key set for Flask application")

app.config.update(
    SECRET_KEY=SECRET_KEY,
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_CUSTOM=True,
    DROPZONE_ALLOWED_FILE_TYPE='.ttf, .otf',
    DROPZONE_MAX_FILE_SIZE=25,
    DROPZONE_MAX_FILES=1,
    DROPZONE_ENABLE_CSRF=True  # enable CSRF protection
)

dropzone = Dropzone(app)
csrf = CSRFProtect(app)  # initialize CSRFProtect


@app.route('/', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        tt = TTFont(f)
        # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')


# handle CSRF error
@app.errorhandler(CSRFError)
def csrf_error(e):
    return e.description, 400


if __name__ == '__main__':
    app.run(debug=False)
