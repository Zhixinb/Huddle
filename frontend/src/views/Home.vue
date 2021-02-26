<template>
  <v-container fluid pa-0>
      <app-nav></app-nav>
      <div class="col-md-6 offset-md-3">
        <v-card>
            <h1 class="pb-6 text-center">Welcome to Huddle</h1>
          <!-- Uncomment if need to test/change uid  -->
            <!-- <v-text-field
            label="User"
            placeholder="uid"
            v-model="curr_uid"
            outlined
            ></v-text-field>
            <h3> Current UID: {{uid}} </h3> -->
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
import { mapMutations, mapState } from 'vuex'
import AppNav from '@/components/app/Nav'
import CreateForm from '@/components/forms/CreateForm'
import JoinForm from '@/components/forms/JoinForm'
import dbHelper from '../db'
import sessionTracking from '@/mixins/sessionTracking'

export default {
  name: 'Home',
  data: () => ({
    selected_id: '',
    // curr_uid: ''
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
    },
    async redirectToLogin() {
      this.$router.push({ name: 'Login'})
    }
  },
  created() {
    if (this.$store.getters.uid === null) {
        this.redirectToLogin();
    } else {
      // console.log("user is logged in")
    }

    dbHelper.logMetric(this.$options.name)
  },
  computed: {
    ...mapState(['uid'])
  },
  // watch: {
  //   curr_uid: {
  //     handler (newVal) {
  //       this.$store.commit('set_uid', this.curr_uid)
  //     }
  //   }
  // },
  mixins: [sessionTracking]
}
</script>
