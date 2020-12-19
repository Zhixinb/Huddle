<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <v-text-field
            label="User"
            placeholder="uid"
            v-model="curr_uid"
            outlined
          ></v-text-field>
          <h3> Current uid: {{uid}} </h3>
      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState} from 'vuex'

export default {
  data: () => ({
    curr_uid: ''
  }),
  computed: {
    ...mapState(['uid'])
  },
  watch: {
    curr_uid: {
      handler (newVal) {
        this.$store.commit('set_uid', this.curr_uid)
      }
    }
  }
}
</script>
