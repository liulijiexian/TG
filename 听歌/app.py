from flask import Flask, request, render_template, url_for, redirect
from project_code.music_code import Controller
import json

app = Flask(__name__)
c = Controller()

@app.route('/', methods=['GET'])
def index():  # put application's code here
    return render_template('index.html')

@app.route('/getMusicMain', methods=['GET'])
def getMusic():  # put application's code here
    key = request.args.get('key')
    pn = request.args.get('pn')
    rn = request.args.get('rn')

    if pn == '0':
        pn = '1'

    if key:
        content = c.musicListMain(key, pn, rn)
        return render_template('content.html', content=content, key=key, pn=int(pn), rn=rn)
    return render_template('content.html', content=[], key=key, pn=int(pn), rn=rn)

@app.route('/getMusicUrl', methods=['GET'])
def getMusicUrl():  # put application's code here
    rid = request.args.get('rid')

    if rid:
        url = c.getMusicMain(rid)
        return json.dumps({'url': url, 'status': 200})
    return json.dumps({'url': '', 'status': 404})


@app.route('/getMusicMainLrc', methods=['GET'])
def getMusicMainLrc():
    musicId = request.args.get('musicId')

    if musicId:
        lrclist = c.getMusicMainLrc(musicId)
        return json.dumps({'lrclist': lrclist, 'status': 200})
    return json.dumps({'lrclist': '', 'status': 404})


if __name__ == '__main__':
    app.run(debug=True,
            host='0.0.0.0',
            port=5000,
            )



