/**
 * @name Class163
 * @description Lx Music网易云源，由Class163_NexT_API驱动
 * @version 1.0.4
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
  console.log(url)
  request(url, options, (err, resp) => {
    if (err) return reject(err)
    resolve(resp.body)
  })
})

const apis = {
  wy: {
    musicUrl({ songmid }, quality) {
      console.log(`Searching ${songmid} in quality ${quality}`)
      requestUrl = `https://api.u59138.nyat.app:36163/api/lx_service/get?id=${songmid}&quality=${quality}`
      
      return httpRequest(requestUrl).then(data => {
        console.log(data.url)
        return data.url
      })
    },
  }
}

on(EVENT_NAMES.request, ({ source, action, info }) => {
  switch (action) {
    case 'musicUrl':
      return apis[source].musicUrl(info.musicInfo, qualitys[source][info.type]).then(result => {
        return result
      }).catch(err => {
        return Promise.reject(err)
      })
  }
})

send(EVENT_NAMES.inited, {
  openDevTools: false, // 是否打开开发者工具，方便用于调试脚本
  sources: { // 当前脚本支持的源
    wy: { // 支持的源对象，可用 key 值：kw/kg/tx/wy/mg/local
      name: '网易云音乐',
      type: 'music',  // 目前固定为 music
      actions: ['musicUrl'], // 除了 local 外，其他的固定为 ['musicUrl']
      qualitys: ['128k', '320k', 'flac', 'flac24bit'], // 当前脚本的该源所支持获取的 Url 音质，有效的值有：['128k', '320k', 'flac', 'flac24bit']
    },
  },
})
