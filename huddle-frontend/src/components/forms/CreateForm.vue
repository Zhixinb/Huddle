<template>
  <v-fade-transition appear>
    <v-form
      @submit.prevent="createWorkspace"
      id="create-form"
      ref="form"
    >
      <div class="pr-6 pl-6 pb-6">
        <v-card-actions>
          <v-btn
            block
            color="primary"
            large
            type="submit"
            id="create-btn"
          >New Workspace</v-btn>
        </v-card-actions>
      </div>
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
