<template>
  <v-container>
    <app-nav></app-nav>
    <create-form></create-form>
    <join-form></join-form>
    <list-form></list-form>
  </v-container>
</template>

<script>
import { mapMutations } from 'vuex'
import AppNav from '@/components/app/Nav'
import CreateForm from '@/components/forms/CreateForm'
import JoinForm from '@/components/forms/JoinForm'
import ListForm from '@/components/forms/ListForm'

export default {
  name: 'Home',
  components: {
    AppNav,
    CreateForm,
    JoinForm,
    ListForm
  },
  mounted () {
    this.reset_error()
  },
  methods: {
    ...mapMutations(['reset_error'])
  }
}
</script>
