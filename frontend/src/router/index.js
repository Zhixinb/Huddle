import Vue from 'vue'
import Router from 'vue-router'
import LandingPage from '@/views/LandingPage'
import Home from '@/views/Home'
import Workspace from '@/views/Workspace'
import ErrorPage from '@/views/ErrorPage'
import Login from '@/views/Login'
import Analytics from '@/views/Analytics'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'LandingPage',
      component: LandingPage
    },
    {
      path: '/home',
      name: 'Home',
      component: Home
    },
    {
      path: '/workspace/:room',
      name: 'Workspace',
      component: Workspace
    },
    {
      path: '/error',
      name: 'Error',
      component: ErrorPage
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/analytics',
      name: 'Analytics',
      component: Analytics
    }
  ]
})
