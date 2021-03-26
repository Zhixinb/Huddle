<template>
  <v-container style="width: max-content;">
    
    <v-menu
        left
        bottom
        offset-y 
        nudge-width
      >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
            >           
            <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
        </template>

        <v-list>
            <v-list-item disabled>
                <v-list-item-title>User: {{email}}</v-list-item-title>
            </v-list-item>
          <logout-list-item></logout-list-item>      
          <download-list-item> </download-list-item>
          <upload-menu></upload-menu>
        </v-list>
      </v-menu>
  </v-container>
</template>

<script>
import LogoutListItem from './LogoutListItem.vue'
import HotkeyMenu from './HotkeyMenu.vue'
import UploadMenu from './UploadMenu.vue'
import DownloadListItem from './DownloadListItem.vue'
import { mapState } from 'vuex'

export default {
    components: {
        LogoutListItem,
        HotkeyMenu, 
        UploadMenu, 
        DownloadListItem
    },
    computed: {
        ...mapState(['email'])
    }
}
</script>

<style>

</style>