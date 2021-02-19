<template>

  <v-app-bar color="light-blue accent-4" dense>
    <v-btn icon @click='redirectToHome'><v-icon>mdi-home</v-icon></v-btn>
    <v-spacer></v-spacer>
    <user-dropdown></user-dropdown>
  </v-app-bar>
</template>

<script>

import UserDropdown from './UserDropdown.vue'

export default {
  components: { UserDropdown },    
  methods: {
    redirectToHome() {
      if (this.$route.path !== '/home') {
        this.$router.push({ name: 'Home'})
      }
    }
  }
}
</script>
