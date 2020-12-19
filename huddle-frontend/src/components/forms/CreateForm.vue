<template>
  <v-fade-transition appear>
    <v-form
      @submit.prevent="createWorkspace"
      id="create-form"
      ref="form"
    >
      <v-card>
        <v-card-actions>
          <v-btn
            block
            color="primary"
            large
            type="submit"
            id="create-btn"
          >New Workspace</v-btn>
        </v-card-actions>
      </v-card>
    </v-form>
  </v-fade-transition>
</template>

<script>

export default {
  name: 'create-form',
  methods: {
    createWorkspace () {
      this.$refs.form.validate()

      const params = {
        uid: this.$store.getters.uid
      }

      this.$socket.emit('create', params)
    }
  }
}
</script>
