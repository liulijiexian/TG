import requests
import copy


''' 公共请求头  '''
class Headers:
    headers = {
        'UserAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
    }

    session = requests.session()


''' 获取音乐地址模块 '''
class GetMusic(Headers):
    # 初始化
    def __init__(self):
        self.__headers = copy.deepcopy(self.headers)

        self.__session = self.session

    # get请求，获取歌曲
    def get(self, mid, url='http://www.kuwo.cn/api/v1/www/music/playUrl', **kwargs):
        params = {
            'mid': mid,  # 音乐id
            'type': 'convert_url3',  # 类型，不用改
            # 'httpsStatus': '1',
            'br': '320kmp3',  # 在线音乐的比特率，越大则音质越高，可选的有 128kmp3、 192kmp3 和 320kmp3
        }
        return self.__session.get(url, params=params, headers=self.__headers, **kwargs).json()

    # 获取歌词lrc文件
    def getlrc(self, mid, url='http://m.kuwo.cn/newh5/singles/songinfoandlrc', **kwargs):
        params = {
            'musicId': mid,  # 音乐id
            'httpsStatus': '1',
        }
        return self.__session.get(url, params=params, headers=self.__headers, **kwargs).json()

    # 更新请求头
    def upheaders(self, headers):
        self.__headers = headers




''' 获取歌曲列表 '''
class MusicList(Headers):
    def __init__(self):
        self.__headers = copy.deepcopy(self.headers)

        self.__params = {
            'key': '',  # 歌名
            'pn': 1,  # 页数
            'rn': 30,  # 每一页获取的数据个数
        }

        self.__session = self.session
        self.__url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?'

        self.__session = self.session


    def get(self, key, pn=1, rn=30, **keyword):
        self.upkey(key, pn, rn)

        # 获取kw_token，反反爬措施
        req = self.__session.get(f'http://www.kuwo.cn/search/list?key={key}', headers=self.__headers)
        kw_token = req.cookies.get('kw_token')
        headers = {}
        headers['csrf'] = kw_token
        headers['Cookie'] = 'kw_token=' + str(kw_token)
        headers['Referer'] = req.url
        self.upheaders(**headers)

        return self.__session.get(self.__url, params=self.__params, headers=self.__headers, **keyword).json()['data']['list']

    # 更新key
    def upkey(self, key, pn=1, rn=30):
        self.__params['key'] = key
        self.__params['pn'] = pn
        self.__params['rn'] = rn

    # 更新请求头
    def upheaders(self, headers=None, **kwargs):
        if headers:
            self.__headers = headers
        else:
            for j, k in kwargs.items():
                self.__headers[j] = k

    # 获取headers
    def get_headers(self):
        return self.__headers


# 控制器
class Controller:
    def __init__(self):
        self.__getMusic = GetMusic()
        self.__musicList = MusicList()

        # 存放音乐名、作者、音乐id 和 时长
        self.__music = []

    # 获取歌曲目录
    def musicListMain(self, key, pn=1, rn=30):
        # print("歌名\t作者\tid\t时长")
        self.__music = []
        for i in self.__musicList.get(key, pn, rn):
            musicDict = {}
            musicDict['name'] = str(i['name']).strip().replace('&nbsp;', ' ')  # 歌名
            musicDict['author'] = str(i['artist']).strip().replace('&nbsp;', ' ')  # 作者
            # musicDict['url'] = self.getMusicMain(i['rid'])  # 音乐url
            musicDict['url'] = i['rid']  # 音乐url
            musicDict['time'] = str(i['songTimeMinutes']).strip().replace('&nbsp;', ' ')  # 时长

            self.__music.append(musicDict)
            # print(f'{i["name"]}\t{i["artist"]}\t{i["rid"]}\t{i["songTimeMinutes"]}')

        return self.__music

    # 获取歌曲对应链接
    def getMusicMain(self, mid, url=None):
        if url:
            return self.__getMusic.get(mid, url)['data']['url']
        return self.__getMusic.get(mid)['data']['url']

    # 获取歌曲对应歌词
    def getMusicMainLrc(self, mid, url=None):
        if url:
            lrclist = self.__getMusic.getlrc(mid, url)['data']['lrclist']
        else:
            lrclist = self.__getMusic.getlrc(mid)['data']['lrclist']
        return lrclist
