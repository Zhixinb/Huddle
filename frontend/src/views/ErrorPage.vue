<template>
  <v-fade-transition appear>
    <v-container fill-height>
      <v-row align='center' justify='center'>
        <v-card class='pa-md-4 mx-lg-auto'>
          <v-card-text>
            <h3>Error : {{msg}}</h3>
          </v-card-text>
        </v-card>
      </v-row>
    </v-container>
  </v-fade-transition>
</template>

<script>
import dbHelper from '../db'
import sessionTracking from '@/mixins/sessionTracking'
export default {
  name: 'ErrorPage',
  data: () => ({
    msg: ''
  }),
  created () {
    this.msg = this.$route.params.msg
    dbHelper.logMetric(this.$options.name)
  },
  mixins: [sessionTracking]
}
</script>
