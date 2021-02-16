<template>
  <v-container>
      <div class="col-md-6 offset-md-3">
        
        <v-card>
            <sign-up-form></sign-up-form>
            <sign-in-form></sign-in-form>
        </v-card>
        <br/>
      </div>
  </v-container>
</template>

<script>

import SignUpForm from '@/components/forms/SignUpForm'
import SignInForm from '@/components/forms/SignInForm'

export default {
  name: 'Login',
  components: {
    SignUpForm,
    SignInForm
  }
}
</script>

<style>

</style>