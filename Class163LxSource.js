/**
 * @name Class163
 * @description [测试中 - 有致命Bug]Class163官方自建Lx Music源
 * @version 0.1.0
 * @author CooooldWind
 */


const { EVENT_NAMES, request, on, send } = globalThis.lx

const qualitys = {
  wy: {
    '128k': '1',
    '320k': '3',
    'flac': '4',
    'flac24bit': '5',
  },
}
const httpRequest = (url, options = {}) => new Promise((resolve, reject) => {
  console.log('=== HTTP 请求 ===')
  console.log('请求 URL:', url)
  console.log('请求选项:', options)
  
  request(url, options, (err, resp) => {
    if (err) {
      console.log('请求错误:', err)
      return reject(err)
    }
    
    console.log('响应状态码:', resp.statusCode)
    console.log('响应头:', resp.headers)
    
    // 检查是否是重定向响应（状态码 301, 302, 303, 307, 308）
    if (resp.statusCode >= 300 && resp.statusCode < 400 && resp.headers && resp.headers.location) {
      // 如果是重定向，返回重定向的 URL
      console.log('检测到重定向，重定向 URL:', resp.headers.location)
      resolve({ url: resp.headers.location })
    } else {
      // 否则返回响应体
      console.log('响应体:', resp.body)
      resolve(resp.body)
    }
  })
})

const apis = {
  wy: {
    musicUrl({ songmid }, quality = '1') {
      console.log('=== 音乐 URL 请求 ===')
      console.log('歌曲 ID:', songmid)
      console.log('音质:', quality)
      
      const requestUrl = `https://frp-bar.com:36163/api/music/file/${songmid}?quality=${quality}`
      console.log('构建的请求 URL:', requestUrl)
      
      return httpRequest(requestUrl).then(data => {
        console.log('请求结果:', data)
        console.log('返回的音乐 URL:', data.url)
        return data.url
      })
    },
  }
}

// 注册应用 API 请求事件
// source 音乐源，可能的值取决于初始化时传入的 sources 对象的源 key 值
// info 请求附加信息，内容根据 action 变化
// action 请求操作类型，目前只有 musicUrl，即获取音乐 URL 链接，
//    当 action 为 musicUrl 时 info 的结构：{type, musicInfo}，
//        info.type：音乐质量，可能的值有 128k / 320k / flac / flac24bit（取决于初始化时对应源传入的 qualitys 值中的一个）
//                   特殊情况：源为 local 时，该值为 null
//        info.musicInfo：音乐信息对象，里面有音乐 ID、名字等信息
on(EVENT_NAMES.request, ({ source, action, info }) => {
  console.log('=== API 请求事件 ===')
  console.log('源:', source)
  console.log('操作:', action)
  console.log('附加信息:', info)
  
  // 被调用时必须返回 Promise 对象
  switch (action) {
    // action 为 musicUrl 时需要在 Promise 返回歌曲 url
    case 'musicUrl':
      console.log('=== 处理音乐 URL 请求 ===')
      console.log('音乐信息:', info.musicInfo)
      console.log('请求音质:', info.type)
      
      let mappedQuality = qualitys[source][info.type]
      console.log('映射后的音质值:', mappedQuality)
      
      // 如果映射后的音质值为 undefined，使用默认值 '1'（128k）
      if (!mappedQuality) {
        console.log('音质映射失败，使用默认值: 1')
        mappedQuality = '3'
      }
      
      return apis[source].musicUrl(info.musicInfo, mappedQuality).then(result => {
        console.log('音乐 URL 请求成功，返回结果:', result)
        return result
      }).catch(err => {
        console.log('音乐 URL 请求失败:', err)
        return Promise.reject(err)
      })
    // action 为 lyric 时需要在 Promise 返回歌词信息
    case 'lyric':
      console.log('=== 处理歌词请求 ===')
      console.log('音乐信息:', info.musicInfo)
      
      return apis[source].musicUrl(info.musicInfo).then(result => {
        console.log('歌词请求成功，返回结果:', result)
        return result
      }).catch(err => {
        console.log('歌词请求失败:', err)
        return Promise.reject(err)
      })
    // action 为 pic 时需要在 Promise 返回歌曲封面 url
    case 'pic':
      console.log('=== 处理封面请求 ===')
      console.log('音乐信息:', info.musicInfo)
      
      return apis[source].musicUrl(info.musicInfo).then(result => {
        console.log('封面请求成功，返回结果:', result)
        return result
      }).catch(err => {
        console.log('封面请求失败:', err)
        return Promise.reject(err)
      })
  }
})

// 脚本初始化完成后需要发送 inited 事件告知应用
// 注意：初始化事件被发送前，执行脚本的过程中出现任何错误将视为脚本初始化失败
send(EVENT_NAMES.inited, {
  openDevTools: true, // 是否打开开发者工具，方便用于调试脚本
  sources: { // 当前脚本支持的源
    wy: { // 支持的源对象，可用 key 值：kw/kg/tx/wy/mg/local
      name: '网易云音乐',
      type: 'music',  // 目前固定为 music
      actions: ['musicUrl'], // 除了 local 外，其他的固定为 ['musicUrl']
      qualitys: ['128k', '320k', 'flac', 'flac24bit'], // 当前脚本的该源所支持获取的 Url 音质，有效的值有：['128k', '320k', 'flac', 'flac24bit']
    },
  },
})
