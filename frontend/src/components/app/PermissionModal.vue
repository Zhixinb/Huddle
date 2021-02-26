<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="500"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          v-bind="attrs"
          v-on="on"
          v-on:click="onClick"
          :disabled='!can_share'
          class='ma-1'
        >
          <v-icon>mdi-account-multiple</v-icon>
          Share
        </v-btn>
      </template>
      <v-card class='pa-4 mx-auto'>
        <v-card-title class="headline">
          Share with people
        </v-card-title>
        <v-form v-on:submit.prevent='addListing' class="flex">
          <v-container fill-height fluid>

            <v-row align="center">
              <v-col cols="5">
                <v-text-field type='text' v-model="new_uid" label='Add user email' hide-details="auto" dense></v-text-field>
              </v-col>
              <v-col cols="4" pa-0 ma-0>
                <v-select
                  v-model="selected_perm_string"
                  :items="perm_strings"
                  menu-props="auto"
                  hide-details="auto"
                  single-line
                  dense
              ></v-select>     
              </v-col>
              <v-col>
                <v-btn type='submit' color='secondary'>Add</v-btn>
              </v-col>
            </v-row>
          </v-container>
        </v-form>
        <ul>
          <li v-for="(listing, index) in whitelist" :key="index">
            <div id='LISTING'>
              <span>
                {{ listing.uid }},  {{getPermissionString(listing.perm, permission_map)}}
              </span>
              <span>
                <v-btn v-on:click="deleteListing(listing)"
                      :disabled='!can_remove(listing.perm)'
                      small>Remove</v-btn>
              </span>
            </div>
          </li>
        </ul>

        <v-switch v-model='globalShareSwitch'>
          <template v-slot:label>
            <v-card-text v-if='globalShareSwitch' >Public</v-card-text>
            <v-card-text v-else>Restricted</v-card-text>
          </template>
        </v-switch>
        
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <v-btn v-clipboard:copy="room"
            v-bind="attrs"
              v-on="on"
                      small>Room code: {{room}}</v-btn>            
          </template>
          <span>Copy to clipboard</span>
        </v-tooltip>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="green darken-1"
            text
            @click="dialog = false"
          >
            Done
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
import {mapState} from 'vuex'
import Vue from 'vue'
import VueClipboard from 'vue-clipboard2'
import dbHelper from '../../db'

VueClipboard.config.autoSetContainer = true
Vue.use(VueClipboard)

export default {
  name: 'PermissonModal',
  data: () => ({
    
    dialog: false,
    new_uid: '',
    selected_perm_string: '',
    new_perm: -1,
    perm_strings: []
  }),
  methods: {
    onClick () {
      const params = {
        uid: this.$store.getters.uid,
        room: this.$route.params.room
      }
      this.$socket.emit('get_share_state', params)
    },
    getPermissionString (perm, map) {
      return Object.keys(map).find(key => map[key] === perm)
    },
    addListing () {
      // TODO: add checks to uid (e.g. not empty, is valid, etc.)
      if (this.new_uid) {
        let listing = {uid: this.new_uid, perm: this.new_perm}
        const params = {
          uid: this.$store.getters.uid,
          room: this.$store.getters.room,
          listing: listing,
          action: 'add'
        }
        console.log("perm to send for updating whitelist:" + JSON.stringify(params))
        this.$socket.emit('update_whitelist', params)
        dbHelper.logMetric("PermissionAdded")
        this.new_uid = '' // clear input        
      }
    },
    deleteListing (listing) {
      const params = {
        uid: this.$store.getters.uid,
        room: this.$store.getters.room,
        listing: listing,
        action: 'remove'
      }
      this.$socket.emit('update_whitelist', params)
      dbHelper.logMetric("PermissionRemoved")
    },
    can_remove (perm) {
      // Allow removal up to own permission level, excluding OWNER
      if (perm === this.permission_map['OWNER']) {
        return false
      } else {
        let role = this.role
        let currPerm = this.permission_map[role]
        return currPerm <= perm
      }
    }
  },
  computed: {
    ...mapState('ws', ['whitelist', 'global_share_state', 'permission_map', 'can_share', 'role']),
    ...mapState(['room']),
    globalShareSwitch: {
      get () {
        return this.global_share_state !== this.permission_map.PERM_DENIED
      },
      set (v) {
        const params = {
          uid: this.$store.getters.uid,
          room: this.$store.getters.room,
          new_state: v
        }
        this.$socket.emit('set_global_share_state', params)
      }
    }
  },
  watch: {
    can_share (newState) {
      if (!newState) {
        this.dialog = false
      }
    },
    global_share_state (newState) {
      const params = {
        uid: this.$store.getters.uid,
        room: this.$route.params.room
      }
      this.$socket.emit('get_share_state', params)
    },
    selected_perm_string (newState) {
      this.new_perm = this.permission_map[newState]
    }
  },
  created() {
    // TODO: check user's permssion level and remove/modify the perm_strings to remove disallowed perms
    // this.perm_strings = Object.keys(this.permission_map)
    this.perm_strings = ['EDITOR', 'VIEWER']
    this.selected_perm_string = 'VIEWER'
    this.new_perm = 2
  }
}
</script>

<style>
.flex {
  display: flex;
}
#LISTING {
  display: flex;
  justify-content: space-between;
  padding: 5px;
}
</style>
