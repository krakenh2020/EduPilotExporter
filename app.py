import os
from logging.config import dictConfig

from flask import Flask, request, abort
from itsdangerous import SignatureExpired, TimedSerializer
from werkzeug.utils import secure_filename

app = Flask(__name__)

TOKEN_SECRET_KEY = "foobar"
TOKEN_HEADER_NAME = "X-KRAKEN-TOKEN"
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

    if TOKEN_HEADER_NAME not in request.headers:
        abort(400, 'No {} header found in request.'.format(TOKEN_HEADER_NAME))

    authHeader = request.headers.get(TOKEN_HEADER_NAME)
    s = TimedSerializer(TOKEN_SECRET_KEY)
    try:
        tokenData, ts = s.loads(authHeader, max_age=TOKEN_MAX_AGE, return_timestamp=True)
    except SignatureExpired as err:
        abort(400, 'Token invalid: {}'.format(err))

    if request.method == 'POST':
        if 'type' not in request.args or 'id' not in request.args:
            abort(400, 'No type and/or id GET parameter found in request.')

        if 'credential' not in request.files:
            abort(400, 'No credential file found in request.')

        credential = request.files['credential']
        filetype = secure_filename(request.args.get('type'))
        filename = '{}.json'.format(secure_filename(request.args.get('id')))
        os.makedirs(os.path.join(uploads_dir, filetype), exist_ok=True)
        storagePath = os.path.join(uploads_dir, filetype, filename)
        if os.path.isfile(storagePath):
            abort(406, 'Credential already exists: {}/{}'.format(filetype, filename))

        credential.save(storagePath)

        return 'Upload OK: {}'.format(filename)

    return 'Use the POST system.'


if __name__ == '__main__':
    app.logger.info('Initializing app ...')
    app.run()
