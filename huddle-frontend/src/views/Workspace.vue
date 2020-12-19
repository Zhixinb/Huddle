<template>
  <v-fade-transition appear>
    <v-card>
      <div>
          <h3>Workspace ID : {{workspace}}</h3>
          <h2>Role: {{role}} </h2>
          <permission-modal/>

      </div>
    </v-card>
  </v-fade-transition>
</template>

<script>
import {mapState, mapMutations} from 'vuex'
import PermissionModal from '@/components/app/PermissionModal'

export default {
  name: 'Workspace',
  components: {
    PermissionModal
  },
  data: () => ({
    curr_room_id: ''
  }),
  beforeMount () {
    const params = {
      uid: this.$store.getters.uid,
      room: this.$store.getters.room,
      sid: this.$store.getters.sid
    }
    this.$socket.emit('join', params)
    this.$socket.emit('get_share_state', params)
  },
  computed: {
    ...mapState(['workspace']),
    ...mapState('ws', ['role'])
  },
  beforeDestroy () {
    const params = {
      uid: this.$store.getters.uid,
      room: this.workspace.workspace_id
    }
    this.$socket.emit('leave', params)
  },
  methods: {
    ...mapMutations(['set_room'])
  }
}
</script>
