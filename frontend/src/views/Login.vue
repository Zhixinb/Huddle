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
import dbHelper from '../db'
import sessionTracking from '@/mixins/sessionTracking'
export default {
  name: 'Login',
  components: {
    SignUpForm,
    SignInForm
  },
  created() {
    dbHelper.logMetric(this.$options.name)
  },
  mixins: [sessionTracking]
}
</script>

<style>

</style>