import requests
from itsdangerous import TimestampSigner, TimedSerializer

url = 'http://127.0.0.1:5000/upload'

SECRET_KEY = "fooKRAKENbar"


def upload(filename, type, id):
    s = TimedSerializer(SECRET_KEY, signer=TimestampSigner)
    token = s.dumps('KRAKEN')
    print(token)

    headers = {'Authorization': token}
    parameters = {'id': id,
                  'type': type}
    files = {'credential': open(filename, 'r')}
    r = requests.post(url, files=files, headers=headers, params=parameters)
    print(r.text)


if __name__ == '__main__':
    upload('testfiles/test1.txt', 'grade', 'bsc')
