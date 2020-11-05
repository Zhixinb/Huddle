<template>
  <v-fade-transition appear>
    <v-card>
      <h3> List of Rooms </h3>
      <ul id="workspace-list">
          <li v-for="(ws_id, index) in workspace_list" :key="index">
          {{ ws_id }}
          </li>
      </ul>
    </v-card>
  </v-fade-transition>
</template>

<script>

import {mapState} from 'vuex'

export default {
  name: 'list-form',
  computed: {
    ...mapState(['workspace_list'])
  }
}
</script>
