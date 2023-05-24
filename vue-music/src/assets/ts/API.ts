import axio from "axios";

/**
 * 全局配置(对全局生效)
 */
// axio.defaults.headers['Content-Type'] = 'application/json';
// axio.defaults.timeout = 3000; // 重写库的超时默认值，现在，所有使用此实例的请求都将等待3秒，然后才会超时
// 创建实例时配置默认值
const axios = axio.create();   // 仅对这一个实例生效
// 创建实例后修改默认值
axios.defaults.headers['Content-Type'] = 'application/json';
axios.defaults.headers['Access-Control-Allow-Origin'] = '*';  // 允许跨域
axios.defaults.timeout = 5000; // 重写超时默认值


// 添加响应拦截器
axios.interceptors.response.use(function (response) {
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    return response.data;
  }, function (error) {
    // 超出 2xx 范围的状态码都会触发该函数。
    // 对响应错误做点什么
    return Promise.reject(error);
  });



const HOST_POST = 'https://xiao-nan-music-house-server.vercel.app';


/**
 * 用于中止上一个同样的请求
 */
const cancels = new Map<string, AbortController>();
function isCancels(key:string){
    const cancel = cancels.get(key);
    if (cancel){
        cancel.abort(); // 中止（取消请求）
        // cancels.delete(key); // 删除（当取消请求时，删除）
    }
    cancels.set(key, new AbortController()); // 新建/修改
}

/**
 * 获取歌曲列表
 * 参数：params: {
 *     key:???, 歌名/歌曲
 *     pn:???,  页数
 *     rn:???  每页歌曲个数
 * }
 */
export function getMusic(key:string, pn:number=1, rn:number=30){
    isCancels('getMusic');
    const a = axios.get(HOST_POST + '/getMusicMain', {
        params: {
            key: key,
            pn: pn,
            rn: rn,
        },
        signal: cancels.get('getMusic')?.signal
    })
    .then((response:any) => {
        return response.data;
    })
    .catch((response) => {
        return response;
    })
    return a;
}


/**
 * 获取歌曲对应链接
 * 参数：params: {
 *     rid: ???, 歌曲rid
 * }
 */
export function getMusicUrl(rid:number){
    isCancels('getMusicUrl');
    const a = axios.get(HOST_POST + '/getMusicUrl', {
        params: {
            rid: rid
        },
        signal: cancels.get('getMusicUrl')?.signal
    })
    .then((response) => {
        return response;
    })
    .catch((response) => {
        return response
    })
    return a;
}


/**
 * 获取歌曲对应歌词
 * 参数：params: {
 *     musicId:???, 歌曲rid
 * }
 */
export function getMusicMainLrc(musicId:number){
    isCancels('getMusicMainLrc');
    const a = axios.get(HOST_POST + '/getMusicMainLrc', {
        params: {
            musicId: musicId
        },
        signal: cancels.get('getMusicMainLrc')?.signal
    })
    .then((response) => {
        return response
    })
    .catch((response) => {
        return response
    })
    return a;
}


/**
 * 登录
 * 参数：
 *     user: ???，用户账号
 */
export function login(user:any){
    isCancels('login');
    const a = axios.post(HOST_POST + '/login', 
    {
        user: user
    },
    {

        signal: cancels.get('login')?.signal
    })
    .then((response) => {
        return response;
    })
    .catch((response) => {
        return response
    })
    return a;
}


/**
 * 修改历史记录
 * 参数：
 *    user: ???，用户账号
 *    data: ???  用户数据
 */
export function historyRecord(user:string, data:any){
    isCancels('historyRecord');
    const a = axios.put(HOST_POST + '/historyRecord', 
    {
        user: user,
        data: data
    },
    {
        signal: cancels.get('historyRecord')?.signal
    })
    .then((response) => {
        return response
    })
    .catch((response) => {
        return response
    })
    return a;
}

// const a = axios.get(HOST_POST + '/getMusicMain', {
//     params: {
//         key: '许嵩',
//         pn: 1,
//         rn: 30,
//     },
// })
// .then((response) => {
//     return response
// })
// .catch((response) => {
//     return 222
// })
// console.log(a);
// const b = getMusic('许嵩');
// console.log(b);
