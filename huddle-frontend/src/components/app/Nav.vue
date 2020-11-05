<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <h3>User: {{sid}}</h3>
      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState} from 'vuex'

export default {
  computed: {
    ...mapState(['sid'])
  }
}
</script>
