import Vue from 'vue'
import Vuex from 'vuex'
import workspaceStore from './modules/workspace_store'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)
export default new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage,
  })],
  modules: {
    ws: workspaceStore
  },
  state: {
    connected: false,
    disconnected: false,
    disconnect_delay: null,

    email: '',
    uid: null,
    sid: null,
    workspace_list: [],
    workspace: {},
    room: '',
    error: null
  },
  getters: {
    sid (state) {
      if (state.sid) {
        return state.sid
      } else {
        return 'Unknown sid'
      }
    },
    uid (state) {
      // If uid is null, then no authenticated user is signed in
      return state.uid
    },
    room (state) {
      if (state.room) {
        return state.room
      } else {
        return 'Unknown room'
      }
    },
    email (state) {
      if (state.email) {
        return state.email
      } else {
        return 'Unknown email'
      }
    }
  },
  mutations: {
    set_connected (state, payload) {
      state.connected = payload
    },
    set_email (state, payload) {
      state.email = payload
    },
    set_sid (state, payload) {
      state.sid = payload
    },
    set_uid (state, payload) {
      state.uid = payload
    },
    set_workspace_list (state, workspaceList) {
      state.workspace_list = workspaceList
    },
    set_workspace (state, workspace) {
      state.workspace = workspace
    },
    set_room (state, room) {
      state.room = room
    },
    set_error (state, payload) {
      state.error = payload
    },
    reset_error (state) {
      state.room = null
      state.error = null
    }
  },
  actions: {
    WS_connect (context) {
      context.commit('set_connected', true)
      // set sids
      context.commit('set_sid', Vue.prototype.$socket.id)

      // clear disconnect timeout and reconnect
      if (context.state.disconnect_delay) clearTimeout(context.state.disconnect_delay)
      context.state.disconnected = false
    },
    WS_disconnect (context) {
      context.commit('set_connected', false)
      // reset delay timer
      if (context.state.disconnect_delay) clearTimeout(context.state.disconnect_delay)
      context.state.disconnect_delay = setTimeout(() => {
        return (context.state.disconnected = true)
      }, 3000)
    },
    // WS_message corresponds to send() from flask
    WS_message (context, message) {      
      context.commit('reset_error')
      context.commit('set_workspace', message)
      context.commit('set_room', message.workspace_id)
    },
    WS_created_room (context, message) {
      context.commit('reset_error')
      context.commit('set_workspace_list', message.rooms)
      console.log('room:' + JSON.stringify(message.rooms))
    },
    WS_join_room (context, message) {
      context.commit('reset_error')
      context.commit('set_room', message.room)
    },
    WS_error (context, message) {
      context.commit('set_error', message.error)
      console.log('error:' + JSON.stringify(message))
    }
  }
})
