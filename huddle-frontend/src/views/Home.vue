<template>
  <v-container>
      <div class="col-md-6 offset-md-3">
        <v-card>
            <app-nav></app-nav>
            <create-form></create-form>
        </v-card>
        <br/>
        <v-card>
            <join-form :clickedRoom="this.selected_id"></join-form>
        </v-card>
      </div>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex'
import AppNav from '@/components/app/Nav'
import CreateForm from '@/components/forms/CreateForm'
import JoinForm from '@/components/forms/JoinForm'

export default {
  name: 'Home',
  data: () => ({
    selected_id: ''
  }),
  components: {
    AppNav,
    CreateForm,
    JoinForm
  },
  mounted () {
    this.reset_error()
  },
  methods: {
    ...mapMutations(['reset_error']),
    clickedRoom(value) {
        this.selected_id = value;
    }
  }
}
</script>
