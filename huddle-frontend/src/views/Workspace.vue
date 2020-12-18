<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <h3>Workspace ID : {{workspace}}</h3>
          <button type="button" v-on:click="addFormElement('textbox')">Add Textbox</button>
          <button type="button" v-on:click="clear()">Clear Textbox</button>
      </div>
      <div>
        <component v-for="field in fields" v-bind:is="field.type" :key="field.id"></component>
      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState, mapMutations} from 'vuex'
import textbox from '@/components/widgets/textbox'

export default {
  name: 'Workspace',
  components: {
    textbox
  },
  data: () => ({
    fields: [],
    count: 0,
    curr_room_id: ''
  }),
  beforeMount () {
    const params = {
      uid: this.$store.getters.uid,
      room: this.$route.params.room
    }
    this.set_room(this.room_id)
    this.$socket.emit('join', params)
  },
  computed: {
    ...mapState(['workspace'])
  },
  beforeDestroy () {
    const params = {
      uid: this.$store.getters.uid,
      room: this.workspace.workspace_id
    }
    this.$socket.emit('leave', params)
  },
  methods: {
    ...mapMutations(['set_room']),
    addFormElement (type) {
      this.fields.push({
        'type': type,
        id: this.count++
      })
    },
    clear () {
      this.components[0].data.text_content = 'qqqqqqq'
    }
  }
}
</script>
