<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <h3>Workspace ID : {{workspace}}</h3>
          <button type="button" v-on:click="addFormElement('textbox')">Add Textbox</button>
          <button type="button" v-on:click="clear()">Clear Textbox</button>
      </div>
      <div ref="items">
        <component v-for="item in items" v-bind:is="item.type" :key="item.id"></component>
      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState, mapMutations} from 'vuex'
import textbox from '@/components/widgets/textbox'
import workspace from '@/store/workspace'

export default {
  name: 'Workspace',
  components: {
    textbox
  },
  data: () => ({
    //sharedItems: workspace.state,
    // fields: [],
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
    
    // this.$socket.on('room state', function(room_data) {
    //   console.log('here')
    //   for (var key in room_data) {
    //     console.log('text content:' + room_data[key])
    //     this.fields.push({
    //       'type': 'textbox',
    //       'text': room_data[key],
    //       id: key
    //     })
    //     if (key > this.count) {
    //       this.count = key + 1;
    //     }
    //   }
    // })
  },
  // mounted () {
  //   //synchronizes room state
  //   for (var i = 0; i < this.fields.length; i++) {
  //     this.$refs.items.children[i].__vue__.text_content = fields[i].text
  //   }
  // },
  computed: {
    ...mapState(['workspace', 'items'])
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
      // this.fields.push({
      //   'type': type,
      //   'text': '',
      //   id: this.count++
      // })
      // this.items.push({
      //   'type': type,
      //   'text': '',
      //   id: this.count++
      // })
      const params = {
        uid: this.$store.getters.uid,
        room: this.workspace.workspace_id,
        'type': type,
        'text': '',
        id: this.count++,
        action: 'add'
      }
      this.$socket.emit('updateElement', params)
    },
    clear () {
      //this.$emit('onClear', 'qqqqqqq')
      this.$refs.items.children[0].__vue__.clear() 
      //this.components[0].data.text_content = 'qqqqqqq'
    }
    // changeText(text_content) {
    //   this.fields[0].text = text_content
    //   const params = {
    //     uid: this.$store.getters.uid,
    //     room: this.workspace.workspace_id,
    //     key: this.fields[0].id,
    //     text: this.text_content
    //   }
    //   this.$socket.emit('change', params)
    // }
  }
}
</script>
