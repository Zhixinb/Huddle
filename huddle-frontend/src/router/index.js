import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home'
import Workspace from '@/views/Workspace'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/home',
      redirect: '/'
    },
    {
      path: '/workspace/:room',
      name: 'Workspace',
      component: Workspace
    }
  ]
})
