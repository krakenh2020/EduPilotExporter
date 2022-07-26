import os
from logging.config import dictConfig

from flask import Flask, request, abort
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from werkzeug.utils import secure_filename

app = Flask(__name__)

TOKEN_SECRET_KEY = "foobar"
TOKEN_MAX_AGE = 5

uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

dictConfig({
    'version': 1,
    'root': {
        'level': 'INFO',
    }
})


@app.route('/')
def hello_world():  # put application's code here
    return 'KRAKEN Education Pilot Demo: University Batch Data Exporter'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    app.logger.info('Uploading ({})'.format(request.method))

    if request.method == 'POST':
        if 'targettoken' not in request.args:
            abort(400, 'No token parameter found in request.')

        token = request.args.get('targettoken')
        s = URLSafeTimedSerializer(TOKEN_SECRET_KEY)
        try:
            tokenData, ts = s.loads(token, max_age=TOKEN_MAX_AGE, return_timestamp=True)
        except SignatureExpired as err:
            abort(400, 'Token invalid: {}'.format(err))

        if 'credential' not in request.files:
            abort(400, 'No credential file found in request.')

        credential = request.files['credential']
        filename = secure_filename(tokenData)
        storagePath = os.path.join(uploads_dir, filename)
        if os.path.isfile(storagePath):
            abort(406, 'Credential already exists: {}'.format(filename))

        credential.save(storagePath)

        return 'Upload OK: {}'.format(filename)

    return 'Use the POST system.'


if __name__ == '__main__':
    app.logger.info('Initializing app ...')
    app.run()
