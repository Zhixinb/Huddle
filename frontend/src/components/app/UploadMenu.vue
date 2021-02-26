<template>
  <v-dialog
      v-model="dialog"
      persistent
      max-width="400"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-list-item
          v-bind="attrs"
          v-on="on"
          v-on:click="onClick"
          class='ma-1'
        >
          Upload
        </v-list-item>
      </template>
      <v-card class='pa-4 mx-auto'>
        <v-card-title class="headline">
          Upload slides json file
        </v-card-title>


        <v-file-input
        truncate-length="15"
        accept='.json'
        label='File input'
        @change="onUploadFiles"
        ></v-file-input>

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
  name: 'UploadMenu',
  data: () => ({
    dialog: false
  }),
  methods: {
    onClick () {
    },
    onUploadFiles: function(file) {
        console.log(file)
        const params = {
                uid: this.$store.getters.uid,
                room: this.$store.getters.room,
                slides_file: file
        }
        this.$socket.emit('upload_json', params)
    }
  },
  computed: {
    ...mapState('ws', ['whitelist', 'global_share_state', 'permission_map', 'can_share', 'role']),
    ...mapState(['workspace']),
    ...mapState('ws', ['role', 'slides']),
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
