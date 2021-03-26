import { generate_lines } from '../../utils/util.js'
export default ({
  namespaced: true,
  state: {
    whitelist: [],
    global_share_state: -1,
    can_share: false,
    permission_map: {},
    slides: {},
    role: '',
    keymap: {},
    lines: [],
    selected_widgets: [],
    curr_slide_id: 0
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
    },
    keymap (state) {
      return state.keymap
    },
    lines (state) {
      return state.lines
    },
    selected_widgets (state) {
      return state.selected_widgets
    },
    curr_slide_id (state) {
        return state.curr_slide_id
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
    }, 
    set_keymap (state, payload) {
      state.keymap = keymap
    }, 
    set_lines (state, payload) {
      state.lines = payload
    },
    set_selected_widgets(state, payload) {
      state.selected_widgets = payload
    },
    set_curr_slide_id(state, payload) {
        state.curr_slide_id = payload
    }
  },
  actions: {
    WS_share_state_result (context, message) {
      context.commit('set_whitelist', message.whitelist)
      // console.log('whitelist:' + JSON.stringify(message.whitelist))
      
      context.commit('set_global_share_state', message.global_share_state)
      
      context.commit('set_can_share', message.can_share)
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
      // console.log('whitelist:' + JSON.stringify(message.whitelist))
      context.commit('set_global_share_state', message.global_share_state)
      context.commit('set_permission_map', message.permission_map)
      
      if (message.target_uid === context.rootGetters.uid) {
        context.commit('set_role', message.new_role)
        context.commit('set_can_share', message.new_can_share)
      } else {
        context.commit('set_can_share', message.can_share)
      }
    },
    WS_update_slides_result (context, message) {
      if (JSON.stringify(context.getters.slides) !== JSON.stringify(message.new_state)) {
        context.commit('set_slides', message.new_state)
        const slides = context.getters.slides
        const selected_widgets = context.getters.selected_widgets
        const curr_slide_id = context.getters.curr_slide_id
        if (!(curr_slide_id in slides)) {
            context.commit('set_curr_slide_id', Object.keys(slides)[0])
        }
        if ('s_id' in message) {
          if ('c_id' in message) {
            context.commit('set_selected_widgets', selected_widgets.filter(e => e !== message['c_id']))
          }
          var lines = []
          for (var i = 0; i < selected_widgets.length; i++) {
            lines = lines.concat(generate_lines(message['s_id'], selected_widgets[i], slides))
          }
          context.commit('set_lines', lines)
        }
      }
    }
  }
})
