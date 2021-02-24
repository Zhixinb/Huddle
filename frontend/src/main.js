// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import router from './router'
import store from './store'

import App from './App'

import vuetify from '@/plugins/vuetify'
import io from 'socket.io-client'
import VueSocketIO from 'vue-socket.io'

import Amplify from 'aws-amplify';
import awsconfig from './aws-exports'; 
import { firestorePlugin } from 'vuefire'

Vue.use(firestorePlugin)

Amplify.configure(awsconfig);
// window.LOG_LEVEL='DEBUG';
Vue.config.productionTip = false

var hostname = window.location.hostname === 'localhost' ? 'http://127.0.0.1:5000' : 'https://team-huddle.herokuapp.com'

Vue.use(new VueSocketIO({
  debug: true,

  // io('http://127.0.0.1:5000'), // Works for dev

  connection: io(`${hostname}`),
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
