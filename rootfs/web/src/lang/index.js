import { createI18n } from 'vue-i18n'


import customEnUS from './en_US'
import customZhCN from './zh_CN'

const ENUM_LANG = {
  enUS: 'en_US',
  zhCN: 'zh_CN'
}


export const i18n = createI18n({
  locale: ENUM_LANG.zhCN,
  messages: {
    [ENUM_LANG.enUS]: {
      ...customEnUS,
    },
    [ENUM_LANG.zhCN]: {
      ...customZhCN,
    }
  }
})

export const setLang = (lang) => {
  // i18n.global.locale.value = lang
  i18n.global.locale = lang
}

export const getLang = () => {
  // return i18n && i18n.global.locale.value
  return i18n && i18n.global.locale
}

// 获取UA语言类型
export const getUAgentLang = () => {
  const UA = window.navigator.userAgent
  const regx = new RegExp(`LANG/(${ENUM_LANG.enUS}|${ENUM_LANG.zhHK}|${ENUM_LANG.zhCN})`, 'g')
  const result = regx.exec(UA)
  return result ? result[1] : ENUM_LANG.zhCN
}
