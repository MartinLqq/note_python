import Vue from 'vue'
import App from './App.vue'

// 如果from指向一个目录, 会去改目录下找 index.js, 相当于 python 的 __init__.py
import router from './router'
import store from './store'

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
