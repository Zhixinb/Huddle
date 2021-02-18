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
Amplify.configure(awsconfig);

Vue.config.productionTip = false

// var allowedOrigins = "http://localhost:* http://127.0.0.1:*";
// console.log(`//${window.location.host}`)
var hostname = window.location.hostname === 'localhost' ? '127.0.0.1' : window.location.hostname

Vue.use(new VueSocketIO({
  debug: true,
  // http://huddle-backend.us-east-1.elasticbeanstalk.com/
  // io('http://127.0.0.1:5000'), // Works for dev
  // io('http://huddle-backend.us-east-1.elasticbeanstalk.com'),
  // try: io(`//${window.location.host}`), // maybe for production?
  connection: io(`http://${hostname}:5000`),
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
