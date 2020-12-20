export default ({
  namespaced: true,
  state: {
    whitelist: [],
    global_share_state: -1,
    can_share: false,
    permission_map: {},
    slides: [],
    role: ''
  },
  getters: {
    whitelist (state) {
      return state.whitelist
    },
    global_share_state (state) {
      return state.global_share_state
    },
    can_share (state) {
      return state.can_share
    },
    permission_map (state) {
      return state.permission_map
    },
    slides (state) {
      return state.slides
    }
  },
  mutations: {
    set_whitelist (state, payload) {
      state.whitelist = payload
    },
    set_global_share_state (state, payload) {
      state.global_share_state = payload
    },
    set_can_share (state, payload) {
      state.can_share = payload
    },
    set_permission_map (state, payload) {
      state.permission_map = payload
    },
    set_role (state, payload) {
      state.role = payload
    },
    set_slides (state, payload) {
      state.slides = payload
    }
  },
  actions: {
    WS_share_state_result (context, message) {
      context.commit('set_whitelist', message.whitelist)
      console.log('whitelist:' + JSON.stringify(message.whitelist))
      if (JSON.stringify(context.getters.global_share_state) !== JSON.stringify(message.global_share_state)) {
        context.commit('set_global_share_state', message.global_share_state)
      }
      if (JSON.stringify(context.getters.can_share) !== JSON.stringify(message.can_share)) {
        context.commit('set_can_share', message.can_share)
      }
      context.commit('set_permission_map', message.permission_map)
      context.commit('set_role', message.role)
    },
    WS_set_global_share_state_result (context, message) {
      if (JSON.stringify(context.getters.global_share_state) !== JSON.stringify(message.result)) {
        context.commit('set_global_share_state', message.result)
      }
    },
    WS_update_whitelist_result (context, message) {
      context.commit('set_whitelist', message.whitelist)
      console.log('whitelist:' + JSON.stringify(message.whitelist))
      context.commit('set_global_share_state', message.global_share_state)
      context.commit('set_can_share', message.can_share)
      context.commit('set_permission_map', message.permission_map)

      if (message.target_uid === context.rootGetters.uid) {
        context.commit('set_role', message.new_role)
        context.commit('set_can_share', message.new_can_share)
      }
    },
    WS_update_slides_result (context, message) {
      if (JSON.stringify(context.getters.slides) !== JSON.stringify(message.new_state)) {
        context.commit('set_slides', message.new_state)
      }
    }
  }
})
