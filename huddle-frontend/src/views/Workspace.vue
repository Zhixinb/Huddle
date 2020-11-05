<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <h3>Workspace ID : {{workspace}}</h3>
      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState} from 'vuex'

export default {
  name: 'Workspace',
  computed: {
    ...mapState(['workspace'])
  }
}
</script>
