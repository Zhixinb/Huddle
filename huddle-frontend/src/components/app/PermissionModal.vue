<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="primary"
          v-bind="attrs"
          v-on="on"
          v-on:click="onClick"
          :disabled='!can_share'
        >
          Share
        </v-btn>
      </template>
      <v-card class='pa-4 mx-auto'>
        <v-card-title class="headline">
          Share with people
        </v-card-title>
        <v-form v-on:submit.prevent='addListing' class="flex">
          <v-text-field type='text' v-model='new_uid'></v-text-field>
          <v-btn type='submit' color='secondary' large>Add</v-btn>
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
export default {
  name: 'PermissonModal',
  data: () => ({
    dialog: false,
    new_uid: '',
    new_perm: 1 // TODO: add perm dropdown with proper perm promotion rules (e.g. can only promote up to own role's level, exclude OWNER)
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
        this.$socket.emit('update_whitelist', params)

        this.new_uid = '' // clear input
      // this.new_perm = '' // TODO: undo comment when dynamically choosing perm level
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
    }
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
