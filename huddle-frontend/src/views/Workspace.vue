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

import {mapState} from 'vuex'
import textbox from '@/components/widgets/textbox'

export default {
  name: 'Workspace',
  components: {
    textbox
  },
  data: () => ({
    fields: [],
    count: 0
  }),
  computed: {
    ...mapState(['workspace'])
  },
  methods: {
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
