from flask import Flask, request, url_for, redirect
from flask_cors import CORS  # 跨域设置

from project_code.music_code import Controller as music_Controller
from project_code.mongodb_code import Controller as mongodb_Controller

import json

app = Flask(__name__)

# 全局的api接口配置
CORS(app,
     supports_credentials=True)  # 默认情况下，不允许跨站点提交Cookie，如果你希望服务器允许用户跨源发出Cookie或经过身份验证的请求，那只需把supports_credentials 设置为True即可

music_controller = music_Controller()
mongodb_controller = mongodb_Controller('mongoFlaskVue', 'userInfo').musicFlakeVue


@app.errorhandler(404)
def page_not_found(e):
    return '资源不存在404'


@app.errorhandler(500)
def internal_server_error(e):
    return '遇到意外的情况并阻止其执行请求500'


@app.route('/getMusicMain', methods=['GET'])
def getMusic():  # 获取歌曲列表
    key = request.args.get('key')
    pn = request.args.get('pn')
    rn = request.args.get('rn')

    if pn == '0':
        pn = '1'

    if key:
        content = music_controller.musicListMain(key, pn, rn)
        return json.dumps({'data': content, 'status': 200})
    return json.dumps({'data': [], 'status': 404})


@app.route('/getMusicUrl', methods=['GET'])
def getMusicUrl():  # 获取指定歌曲
    rid = request.args.get('rid')

    if rid:
        url = music_controller.getMusicMain(rid)
        return json.dumps({'url': url, 'status': 200})
    return json.dumps({'url': '', 'status': 404})


@app.route('/getMusicMainLrc', methods=['GET'])
def getMusicMainLrc():  # 获取歌词，只能中国大陆IP
    musicId = request.args.get('musicId')

    if musicId:
        lrclist = music_controller.getMusicMainLrc(musicId)
        return json.dumps({'lrclist': lrclist, 'status': 200})
    return json.dumps({'lrclist': '', 'status': 404})


@app.route('/login', methods=['POST'])
def login():  # 登录
    if request.content_type.startswith('application/json'):
        # comment = request.get_json()["content"]
        user = request.json.get('user')
    elif request.content_type.startswith('multipart/form-data'):
        user = request.form.get('user')
    else:
        user = request.values.get("user")

    if user:
        user_data = mongodb_controller.get_one(user)
        if len(user_data) != 0:
            return json.dumps({'userData': user_data, 'status': 200})
    return register_from(user)  # 自动注册


# 注册
def register_from(user):
    user_data = mongodb_controller.insert_one(user, [])
    if len(user_data) != 0:
        return json.dumps({'userData': user_data, 'status': 200})
    return json.dumps({'userData': '', 'status': 404})


@app.route('/register', methods=['POST'])
def register():  # 注册
    if request.content_type.startswith('application/json'):
        # comment = request.get_json()["content"]
        user = request.json.get('user')
    elif request.content_type.startswith('multipart/form-data'):
        user = request.form.get('user')
    else:
        user = request.values.get("user")

    if user:
        return register_from(user)
    return json.dumps({'userData': '', 'status': 404})


@app.route('/historyRecord', methods=['put'])
def history_record():  # 修改历史记录
    if request.content_type.startswith('application/json'):
        # comment = request.get_json()["content"]
        user = request.json.get('user')
        data = request.json.get('data')
    elif request.content_type.startswith('multipart/form-data'):
        user = request.form.get('user')
        data = request.form.get('data')
    else:
        user = request.values.get("user")
        data = request.values.get('data')

    if user:
        if (data == 'delete'):
            result = mongodb_controller.update_one(user, [])
        else:
            user_data = mongodb_controller.get_one(user)
            if (len(user_data) != 0):
                user_data = user_data['data']
                user_data.append(data)
                mongodb_controller.update_one(user, user_data)
                return json.dumps({'status': 200, 'result': 1})
    return json.dumps({'status': 404, 'result': 0})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
    # app.run(debug=True, host='127.0.0.1', port=9090)
