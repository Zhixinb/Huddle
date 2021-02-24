<template>
  <v-app>
      analytics at its finest {{documents}}
  </v-app>
</template>

<script>
import dbHelper, { db } from '../db'
import firebase from 'firebase/app'
import 'firebase/firestore'
import sessionTracking from '@/mixins/sessionTracking'
export default {
    name: 'Analytics',
    data() {
        return {
        documents: [],
        }
    },

    firestore: {
        documents: db.collection('pageviews')
    },
    created() {
        dbHelper.logMetric(this.$options.name)
    },
    mixins: [sessionTracking]
}
</script>

<style>

</style>