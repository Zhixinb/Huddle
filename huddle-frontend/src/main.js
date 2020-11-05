// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import store from './store'

import App from './App'

import vuetify from '@/plugins/vuetify'
import io from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

Vue.config.productionTip = false

Vue.use(new VueSocketIO({
  debug: true,
  connection: io('http://127.0.0.1:5000'),
  vuex: {
    store,
    actionPrefix: 'WS_',
    mutationPrefix: 'WS_'
  }
}))

/* eslint-disable no-new */
new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
