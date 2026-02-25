/**
 * @name Class163
 * @description Lx Music网易云源，由Class163_NexT_API驱动
 * @version 1.0.1
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
  request(url, options, (err, resp) => {
    if (err) {
      return reject(err)
    }
    if (resp.statusCode >= 300 && resp.statusCode < 400 && resp.headers && resp.headers.location) {
      resolve({ url: resp.headers.location })
    } else {
      resolve(resp.body)
    }
  })
})

const apis = {
  wy: {
    musicUrl({ songmid }, quality = '1') {
      const requestUrl = `https://api.u59138.nyat.app:36163/api/music/file/${songmid}?quality=${quality}`
      return httpRequest(requestUrl).then(data => {
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
