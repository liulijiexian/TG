import { ref } from 'vue'
import { defineStore } from 'pinia'

import { getMusic, getMusicMainLrc, getMusicUrl, login, historyRecord } from "@/assets/ts/API";

export const useCounterStore = defineStore('counter', () => {
  const nowMusicInfo = ref();  // 当前播放歌曲的信息
  const musicList = ref<Array<any>>([]);  // 歌曲列表
  const lrclist = ref('');  // 当前播放歌曲的歌词
  const musicUrl = ref();  // 当前歌曲url
  const userInfo = ref();  // 用户信息（如果登录，包含历史记录）
  const isUser = ref(false);  // 是否登录

  /**
   * 获取歌曲列表
   */
  function get_Music(key: string, pn: number = 1, rn: number = 30) {
    // 由于返回的是一个promise值，只能用then这种办法读取
    getMusic(key, pn, rn)
      .then((result) => {
        try {
          if (pn == 1) {
            musicList.value = result;
          }
          else {
            result.forEach((element: any) => {
              musicList.value.push(element);
            });
          }
        }
        catch (err) {
          console.log(err);
        }

      });
  }

  /**
   * 获取歌曲对应歌词
   */
  function get_MusicMainLrc() {
    // 由于返回的是一个promise值，只能用then这种办法读取
    getMusicMainLrc(nowMusicInfo.value.url)
      .then((result) => {
        try {
          lrclist.value = '';
          result.lrclist.forEach((e: any) => {
            lrclist.value += formatTime(e.time);
            lrclist.value += e.lineLyric;
            lrclist.value += '\n';
          })
          // lrclist.value = result.lrclist;
        }
        catch {
          lrclist.value = '[00:00.00]暂无歌词';
        }
      });
  }

  /**
   * 分秒转换
   * @param seconds 
   * @returns 
   */
  function formatTime(seconds: any) {
    let minutes: any = Math.floor(seconds / 60);
    const sec = seconds % 60;
    minutes = minutes < 10 ? `0${minutes}` : minutes;
    let formattedSeconds: any = Math.floor(sec / 1);
    let formattedSecondsMinutes: any = Math.floor((sec % 1) * 100);
    formattedSeconds = formattedSeconds < 10 ? `0${formattedSeconds}` : formattedSeconds;
    formattedSecondsMinutes = formattedSecondsMinutes < 10 ? `0${formattedSecondsMinutes}` : formattedSecondsMinutes;
    return `[${minutes}:${formattedSeconds}.${formattedSecondsMinutes}]`;
  }

  /**
   * 获取歌曲url
   */
  function get_MusicUrl() {
    getMusicUrl(nowMusicInfo.value.url)
      .then((result) => {
        try {
          musicUrl.value = result.url;
        }
        catch {

        }
      });
  }

  /**
   * 登录
   */
  function get_login(user: any) {
    login(user)
      .then((result) => {
        try {
          userInfo.value = result.userData;
          if (userInfo.value) {
            isUser.value = true;
            // 临时存储，会话结束的时候，sessionStorage 中的键值对会被清空
            sessionStorage.setItem('user', userInfo.value.user);
          }
        }
        catch {

        }
      });
  }

  /**
   * 修改历史记录
   */
  function get_historyRecord(user: string, data: any) {
    historyRecord(user, data)
      .then((result) => {
        try {

        }
        catch {

        }
      });
  }

  /**
   * 修改nowMusicUid时，自动获取新的歌曲url及歌词
   * newQuestion：当前歌曲信息
   */
  function setNowMusicUid(newQuestion: any) {
    nowMusicInfo.value = newQuestion;

    get_MusicUrl();
    get_MusicMainLrc();
    if (isUser.value) {
      let ab: boolean = true;
      for (let a = 0; a < userInfo.value.data.length; a++) {
        if (userInfo.value.data[a].url === newQuestion.url) {
          userInfo.value.data.splice(a, 1);
          ab = false;
          break;
        }
      }
      if (ab) {
        get_historyRecord(userInfo.value.user, newQuestion);
      }
      userInfo.value.data.unshift(nowMusicInfo.value);
    }
  }

  /**
   * 清空历史记录
   */
  function delete_historyRecord() {
    if (isUser.value) {
      get_historyRecord(userInfo.value.user, 'delete');
      userInfo.value.data = [];
    }
  }


  /**
   * 退出登录
   */
  function delete_login() {
    isUser.value = false;
    sessionStorage.removeItem('user');
    userInfo.value = null;
  }

  if (sessionStorage.getItem('user')) {
    get_login(sessionStorage.getItem('user'));
  }

  return { nowMusicInfo, musicList, lrclist, musicUrl, userInfo, isUser, get_Music, get_MusicMainLrc, get_MusicUrl, get_login, setNowMusicUid, delete_historyRecord, delete_login }
})
