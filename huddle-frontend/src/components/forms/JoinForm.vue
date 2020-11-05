<template>
  <v-fade-transition appear>
    <v-form
      id="join-form"
      ref="form"
      v-model='valid_form'
      @submit.prevent="join_room"
    >
      <v-card>
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
      </v-card>
    </v-form>
  </v-fade-transition>
</template>

<script>

import {mapMutations} from 'vuex'

export default {
  name: 'join-form',
  data: () => ({
    code_length: 5,
    valid_form: false,
    curr_room_id: ''
  }),
  computed: {
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
        console.log('gonna join a room' + this.curr_room_id)

        const params = {
          sid: this.$store.getters.sid,
          room: this.room_id
        }
        console.log('params:' + JSON.stringify(params))
        this.set_room(this.room_id)
        this.$socket.emit('join', params)
        this.$router.push({ name: 'Workspace', params: { room: this.room_id } })
      }
    }
  }
}
</script>
