<template>
  <div class="container">
      <v-btn
            block
            color="primary"
            large
            @click="redirectToLogin">Get Started</v-btn>   
  </div>
</template>

<script>
export default {
    name: 'LandingPage',
    methods: {
        redirectToLogin() {
            this.$router.push({ name: 'Login'})
        }
    } 
}
</script>

<style>

</style>