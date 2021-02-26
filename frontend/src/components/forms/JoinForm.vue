<template>
  <v-fade-transition appear>
    <v-card>
    <v-form
      id="join-form"
      ref="form"
      v-model='valid_form'
      @submit.prevent="join_room"
    >
      <div class="pa-6">
        <v-card-text>
          <v-text-field
            label="Room ID"
            placeholder="Please enter a room code"
            v-model="curr_room_id"
            :rules="rules"
            :counter="code_length"
            outlined
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
            <v-btn
                block
                color="primary"
                large
                type="submit"
                id="join-btn"
                :disabled='!valid_form'
            >join</v-btn>
        </v-card-actions>
      </div>
    </v-form>
    <div class="pb-6 pr-6 pl-6">
      <h3> List of Rooms </h3>
      <v-list rounded style="max-height: 200px" class="overflow-y-auto">
        <v-list-item-group color="primary">
            <v-list-item v-for="(ws_id, index) in workspace_list" :key="index" @click="clicked(ws_id)">
            <v-list-item-icon>
                <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
                <v-list-item-title>{{ ws_id }}</v-list-item-title>
            </v-list-item-content>
            </v-list-item>
        </v-list-item-group>
        </v-list>
    </div>
    </v-card>
  </v-fade-transition>
</template>

<script>
import {mapState, mapMutations} from 'vuex'
import dbHelper from '../../db'

export default {
  name: 'join-form',
  data() {
        return {
            code_length: 5,
            valid_form: false,
            curr_room_id: ''
        }
  },
  computed: {
    ...mapState(['workspace_list']),
    rules () {
      const rules = []
      if (this.code_length) {
        const rule =
            v => (v || '').length === this.code_length || `Code must be of length ${this.code_length}`

        rules.push(rule)
      }

      return rules
    },
    room_id: {
      get () {
        return this.curr_room_id
      },
      set (v) {
        this.curr_room_id = v
      }
    }
  },
  methods: {
    ...mapMutations(['set_room']),
    join_room () {
      this.$refs.form.validate()
      if (this.valid_form) {
        const params = {
          uid: this.$store.getters.uid,
          room: this.room_id
        }
        this.$socket.emit('get_enter_room_perm', params)
        dbHelper.logMetric("JoinRoomBtn")
      }
    },
    clicked(ws_id) {
        this.curr_room_id = ws_id;
    }
  },
  sockets: {
    enter_room_perm_result (data) {
      let canEnter = data.result
      if (canEnter) {
        this.set_room(this.room_id)
        dbHelper.logMetric("JoinRoomSuccess")
        this.$router.push({ name: 'Workspace', params: { room: this.room_id } })
      } else {
        dbHelper.logMetric("JoinRoomError")
        this.$router.push({ name: 'Error', params: { msg: 'No access to Room ' + this.room_id } })
      }
    },
    created() {
      const params = {
          uid: this.$store.getters.uid
        }

      this.$socket.emit('get_rooms', params)
    }
  }
}
</script>
