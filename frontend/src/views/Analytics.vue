<template>
  <!-- <v-app>
      analytics at its finest {{metric}}
      analytics at its finest {{usersession}}
  </v-app> -->
  <v-container fluid pa-0>
      <!-- analytics at its finest {{metric}} -->
    <div class="col-md-6 offset-md-3">
        <v-card>
            <line-chart :chart-data="pageViewMetricCollection"></line-chart>
        </v-card>
    </div>
  </v-container>
</template>

<script>
import dbHelper, { db } from '../db'
import LineChart from '@/components/app/LineChart.js'
import 'firebase/firestore'
import sessionTracking from '@/mixins/sessionTracking'
import moment from 'moment'


export default {
    name: 'Analytics',
    components: {
      LineChart
    },
    data:() => ({        
        metric: [],
        usersession: [],
        pageViewMetricCollection: {}
    }),
    firestore: {
        metric: db.collection('metric'),
        usersession: db.collection('usersession')
    },
    created() {
        dbHelper.logMetric(this.$options.name)
    },
    watch: {
        metric (newMetric) {
            
            let dataSets = this.extractMetrics(newMetric)
            console.log("langin:" + JSON.stringify(dataSets))           

            this.pageViewMetricCollection = {     
                datasets: [
                    {
                    label: "Landing Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true, 
                    data: dataSets["LandingPage"]
                    },
                    {
                    label: "Analytics Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["Analytics"]
                    },
                    {
                    label: "Home Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,  
                    data: dataSets["Home"]
                    },
                    {
                    label: "Login Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true, 
                    data: dataSets["Login"]
                    },
                    {
                    label: "Workspace Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["Workspace"]
                    },
                    {
                    label: "ErrorPage Page Visits",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ErrorPage"]
                    },
                    {
                    label: "Logout Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["LogoutBtn"]
                    },
                    {
                    label: "Permission Added",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["PermissionAdded"]
                    },
                    {
                    label: "Permission Removed",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["PermissionRemoved"]
                    },
                    {
                    label: "Create Room Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["CreateRoomBtn"]
                    },
                    {
                    label: "Join Room Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomBtn"]
                    },
                    {
                    label: "Join Room Success",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomSuccess"]
                    },
                    {
                    label: "Join Room Error",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["JoinRoomError"]
                    },
                    {
                    label: "Signin Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["SigninBtn"]
                    },
                    {
                    label: "Signup Btn Clicked",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["SignupBtn"]
                    },
                    {
                    label: "Component Created",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ComponentCreated"]
                    },
                    {
                    label: "Connection Created",
                    fill: false,
                    tension: 0.1,
                    showLine: true,
                    data: dataSets["ConnectionCreated"]
                    }
                ]
            }
        }
    },
    methods: {
      extractMetrics(newMetric) {
          let dataSets = {}

          newMetric.forEach(metricItem => {
                // Setup an empty array for each metric to push to
                if (!(metricItem.metric in dataSets)) {
                    dataSets[metricItem.metric] = []
                }
                dataSets[metricItem.metric].push({x: moment(metricItem.timestamp_bin), y: metricItem.counter})  
          })

          return dataSets
      }
    },
    mixins: [sessionTracking],
    computed: {
        myStyles () {
            return {
                height: `${this.height}px`,
                position: 'relative'
            }
        }
    }
}
</script>

<style>
 
</style>