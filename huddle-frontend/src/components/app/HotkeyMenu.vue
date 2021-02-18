<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          dark
          small
          v-bind="attrs"
          v-on="on"
          v-on:click="onClick"
          :disabled='!can_share'
          class='ma-1'
          max-width="70"
        >
          Hotkeys
        </v-btn>
      </template>
      <v-card class='pa-4 mx-auto'>
        <v-card-title class="headline">
          Set Hotkeys
        </v-card-title>


        <v-row>
          <p>Save</p>
          <v-text-field type='text' label='Key Binding'></v-text-field>
          <v-btn type='submit' color='secondary' small>Change</v-btn>
        </v-row>

        <v-row>
          <p>Print</p>
          <v-text-field type='text' label='Key Binding'></v-text-field>
          <v-btn type='submit' color='secondary' small>Change</v-btn>
        </v-row>

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
  name: 'HotkeyMenu',
  data: () => ({
    dialog: false
  }),
  methods: {
    onClick () {
    //   const params = {
    //     uid: this.$store.getters.uid,
    //     room: this.$route.params.room
    //   }
      //this.$socket.emit('get_share_state', params)
    }
  },
  computed: {
    ...mapState('ws', ['whitelist', 'global_share_state', 'permission_map', 'can_share', 'role'])
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
